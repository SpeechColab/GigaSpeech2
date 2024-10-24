import argparse
import json
import re
from abc import ABC, abstractmethod
from pathlib import Path

import fasttext
from tqdm import tqdm


class FilterStrategy(ABC):
    @abstractmethod
    def apply(self, line):
        pass


class CharsetFilter(FilterStrategy):
    def __init__(self):
        thai_chars = r"\u0E00-\u0E7F"
        digits = r"\u0030-\u0039"
        blank_symbol = r"\s"
        valid_symbols = thai_chars + digits + blank_symbol
        self.valid_pattern = re.compile(f"[^{valid_symbols}]")

    def apply(self, line):
        return not self.valid_pattern.search(line["text"])


class LanguageConfidenceFilter(FilterStrategy):
    def __init__(self, model_path, confidence_threshold=0.95):
        self.model = fasttext.load_model(model_path)
        self.confidence_threshold = confidence_threshold

    def apply(self, line):
        labels, probabilities = self.model.predict(line["text"], k=1)
        return probabilities[0] >= self.confidence_threshold


class AudioDurationFilter(FilterStrategy):
    def __init__(self, min_keep_duration=1, max_keep_duration=30):
        self.min_keep_duration = min_keep_duration
        self.max_keep_duration = max_keep_duration

    def apply(self, line):
        return (
            line["duration"] >= self.min_keep_duration
            and line["duration"] <= self.max_keep_duration
        )


class ContentFilter:
    def __init__(self, strategies):
        self.strategies = strategies

    def __call__(self, line):
        for strategy in self.strategies:
            if not strategy.apply(line):
                return False
        return True


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--lid-model-path", type=str, required=True)
    return parser.parse_args()


def filter_manifests(input_dir, output_dir, content_filter):
    total_cnt = 0
    valid_cnt = 0
    for manifest_path in tqdm(input_dir.rglob("*.jsonl"), desc="Filtering manifests"):
        filtered_manifest_path = output_dir / ("filtered_" + manifest_path.name)

        with open(manifest_path, "r", encoding="utf-8") as reader, open(
            filtered_manifest_path, "w", encoding="utf-8"
        ) as writer:
            for line in reader:
                line = json.loads(line)
                total_cnt += 1
                if content_filter(line):
                    writer.write(json.dumps(line) + "\n")
                    valid_cnt += 1

    print(
        f"total segments: {total_cnt}, valid segments: {valid_cnt}, filtered rate: {1 - valid_cnt / total_cnt}"
    )


def main():
    args = parse_args()
    strategies = [
        CharsetFilter(),
        LanguageConfidenceFilter(args.lid_model_path, 0.99),
        AudioDurationFilter(2, 30),
    ]
    content_filter = ContentFilter(strategies)
    filter_manifests(args.input_dir, args.output_dir, content_filter)


if __name__ == "__main__":
    main()
