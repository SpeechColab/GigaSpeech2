import argparse
import json
import os

import sox


def main(args):
    os.makedirs(args.output_dir, exist_ok=True)
    audio_id = (
        os.path.basename(args.manifest_filepath)
        .replace("_manifest", "")
        .replace("filtered_", "")
        .split(".")[0]
    )
    segment_dir = os.path.join(args.output_dir, audio_id)
    os.makedirs(segment_dir, exist_ok=True)
    text_file_path = os.path.join(segment_dir, f"{audio_id}.trans.txt")

    with open(args.manifest_filepath, "r") as reader, open(
        text_file_path, "w"
    ) as writer:
        for i, line in enumerate(reader):
            segment_id = f"{audio_id}-{i}"
            line = json.loads(line)

            if line["duration"] < 2 or line["duration"] > 30:
                continue

            audio_filepath = line["audio_filepath"]
            audio_start_sec = line["audio_start_sec"]
            audio_end_sec = audio_start_sec + line["duration"]

            output_file = os.path.join(segment_dir, f"{segment_id}.wav")
            tfm = sox.Transformer()
            tfm.trim(audio_start_sec, audio_end_sec)
            tfm.build_file(audio_filepath, output_file)

            text = line["text"]
            writer.write(segment_id + " " + text + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Segment long audio files")
    parser.add_argument(
        "-m", "--manifest-filepath", type=str, help="Path to manifest file "
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        help="Output directory to store segmented audio files",
    )
    args = parser.parse_args()
    main(args)
