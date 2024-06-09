import argparse
import json
from pathlib import Path

import textgrid


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hyp-dir", type=Path, required=True)
    parser.add_argument("--ref-dir", type=Path, required=True)
    return parser.parse_args()


def calculate_overlap_time(start1, end1, start2, end2):
    return max(0, min(end1, end2) - max(start1, start2))


def calculate_precision(hyp_intervals, ref_intervals):
    total_true_positive_time = 0
    total_predicted_time = 0

    for hyp_start, hyp_end in hyp_intervals:
        hyp_duration = hyp_end - hyp_start
        total_predicted_time += hyp_duration
        overlap_time_with_all_refs = 0

        for ref_start, ref_end in ref_intervals:
            overlap = calculate_overlap_time(hyp_start, hyp_end, ref_start, ref_end)
            overlap_time_with_all_refs += overlap

        total_true_positive_time += overlap_time_with_all_refs

    precision = total_true_positive_time / total_predicted_time

    return precision


def main():
    args = parse_args()

    for ref_path in args.ref_dir.rglob("*.TextGrid"):
        file_id = ref_path.stem
        hyp_path = args.hyp_dir / (file_id + "_manifest.jsonl")

        assert hyp_path.exists(), f"{hyp_path} does not exist."

        tg = textgrid.TextGrid.fromFile(ref_path)
        ref_intervals = []
        for interval in tg[0]:
            if len(interval.mark) > 0:
                start = interval.minTime
                end = interval.maxTime
                ref_intervals.append((start, end))

        hyp_intervals = []
        with open(hyp_path, "r") as f:
            for line in f:
                data = json.loads(line)
                if len(data["text"]) > 0:
                    start = data["audio_start_sec"]
                    duration = data["duration"]
                    end = start + duration
                    hyp_intervals.append((start, end))

        print(file_id, calculate_precision(hyp_intervals, ref_intervals))


if __name__ == "__main__":
    main()
