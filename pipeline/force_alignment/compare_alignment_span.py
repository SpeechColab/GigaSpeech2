import argparse
import json
import os

import textgrid
import torch
import tqdm

# DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def compare_file(ref_path, hyp_path):
    # assert not os.path.exists(
    #     args.outdir
    # ), f"Error: Output path exists already {args.outdir}"

    grid = textgrid.TextGrid.fromFile(ref_path)
    ref_span = [
        (interval.minTime, interval.maxTime, interval.mark)
        for interval in grid.tiers[0].intervals
        if len(interval.mark.strip()) > 0
    ]
    with open(hyp_path, "r") as f:
        lines = f.read().splitlines()
        lines = [json.loads(line) for line in lines]
        hyp_span = [
            (
                item["audio_start_sec"],
                item["audio_start_sec"] + item["duration"],
                item["normalized_text"],
            )
            for item in lines
        ]
    counter = 0
    record = []
    one_word_mismatch = 0
    two_word_mismatch = 0
    for (r_s, r_e, r_m), (h_s, h_e, h_m) in zip(ref_span, hyp_span):
        if r_s >= h_e or r_e <= h_s:
            counter += 1
            record.append(((r_s, r_e, r_m), (h_s, h_e, h_m)))
            if len(r_m.strip().split()) <= 1:
                one_word_mismatch += 1
            if len(r_m.strip().split()) == 2:
                two_word_mismatch += 1
    print(f"The mismatch number of {ref_path} is {counter}")
    for item in record:
        print(item)
    return len(ref_span), len(record), one_word_mismatch, two_word_mismatch


def main(args):
    ref_dir = args.ref
    hyp_dir = args.hyp
    items = os.listdir(ref_dir)
    items = [
        os.path.splitext(item)[0]
        for item in items
        if os.path.splitext(item)[1] == ".TextGrid"
    ]
    ref_count = 0
    mis_match_count = 0
    one_word_mismatch_count = 0
    two_word_mismatch_count = 0
    for item in tqdm.tqdm(items):
        ref_path = os.path.join(ref_dir, f"{item}.TextGrid")
        hyp_path = os.path.join(hyp_dir, f"{item}.jsonl")
        r_n, m_n, o_n, t_n = compare_file(ref_path, hyp_path)
        ref_count += r_n
        mis_match_count += m_n
        one_word_mismatch_count += o_n
        two_word_mismatch_count += t_n
    print(
        f"total: {ref_count}, mismatch: {mis_match_count}, one word mismatch: {one_word_mismatch_count}, two word mismatch: {two_word_mismatch_count}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Align and segment long audio files")
    parser.add_argument("--ref", type=str, help="directory of reference")
    parser.add_argument("--hyp", type=str, help="directory of hypthesis")
    parser.add_argument(
        "-l", "--lang", type=str, default="eng", help="ISO code of the language"
    )
    parser.add_argument(
        "-o",
        "--outdir",
        type=str,
        help="Output directory to store segmented audio files",
    )
    args = parser.parse_args()
    main(args)
