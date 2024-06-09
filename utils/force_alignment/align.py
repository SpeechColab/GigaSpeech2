import argparse
import json
import os

import sox
import torch
import torchaudio
import torchaudio.functional as F

from align_utils import (get_spans, get_uroman_tokens, load_model_dict,
                         merge_repeats, time_to_frame)
from text_normalization import text_normalize

SAMPLING_FREQ = 16000
EMISSION_INTERVAL = 30
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def generate_emissions(model, audio_file):
    waveform, _ = torchaudio.load(audio_file)  # waveform: channels X T
    waveform = waveform.to(DEVICE)
    total_duration = sox.file_info.duration(audio_file)

    audio_sf = sox.file_info.sample_rate(audio_file)
    assert audio_sf == SAMPLING_FREQ

    emissions_arr = []
    with torch.inference_mode():
        i = 0
        while i < total_duration:
            segment_start_time, segment_end_time = (i, i + EMISSION_INTERVAL)

            context = EMISSION_INTERVAL * 0.1
            input_start_time = max(segment_start_time - context, 0)
            input_end_time = min(segment_end_time + context, total_duration)
            waveform_split = waveform[
                :,
                int(SAMPLING_FREQ * input_start_time) : int(
                    SAMPLING_FREQ * (input_end_time)
                ),
            ]

            model_outs, _ = model(waveform_split)
            emissions_ = model_outs[0]
            emission_start_frame = time_to_frame(segment_start_time)
            emission_end_frame = time_to_frame(segment_end_time)
            offset = time_to_frame(input_start_time)

            emissions_ = emissions_[
                emission_start_frame - offset : emission_end_frame - offset, :
            ]
            emissions_arr.append(emissions_)
            i += EMISSION_INTERVAL

    emissions = torch.cat(emissions_arr, dim=0).squeeze()
    emissions = torch.log_softmax(emissions, dim=-1)

    stride = float(waveform.size(1) * 1000 / emissions.size(0) / SAMPLING_FREQ)

    return emissions, stride


def get_alignments(
    audio_file,
    tokens,
    model,
    dictionary,
    use_star,
):
    # Generate emissions
    emissions, stride = generate_emissions(model, audio_file)
    T, N = emissions.size()
    if use_star:
        emissions = torch.cat([emissions, torch.zeros(T, 1).to(DEVICE)], dim=1)

    # Force Alignment
    if tokens:
        token_indices = [
            dictionary[c] for c in " ".join(tokens).split(" ") if c in dictionary
        ]
    else:
        print(f"Empty transcript!!!!! for audio file {audio_file}")
        token_indices = []

    blank = dictionary["<blank>"]

    targets = torch.tensor(token_indices, dtype=torch.int32).to(DEVICE)

    input_lengths = torch.tensor(emissions.shape[0]).unsqueeze(-1)
    target_lengths = torch.tensor(targets.shape[0]).unsqueeze(-1)
    path, _ = F.forced_align(
        emissions.unsqueeze(0),
        targets.unsqueeze(0),
        input_lengths,
        target_lengths,
        blank=blank,
    )
    path = path.squeeze().to("cpu").tolist()

    segments = merge_repeats(path, {v: k for k, v in dictionary.items()})
    return segments, stride


def main(args):
    raw_transcripts = []
    with open(args.text_filepath) as f:
        raw_transcripts = [line.strip() for line in f]
    print("Read {} lines from {}".format(len(raw_transcripts), args.text_filepath))

    transcripts = []
    norm_transcripts = []
    for line in raw_transcripts:
        transcript, norm_transcript = text_normalize(line.strip(), args.lang)
        if len(norm_transcript) > 0:
            transcripts.append(transcript)
            norm_transcripts.append(norm_transcript)
    tokens = get_uroman_tokens(norm_transcripts, args.uroman_path, args.lang)

    model, dictionary = load_model_dict()
    model = model.to(DEVICE)
    if args.use_star:
        dictionary["<star>"] = len(dictionary)
        tokens = ["<star>"] + tokens
        transcripts = ["<star>"] + transcripts
        norm_transcripts = ["<star>"] + norm_transcripts

    segments, stride = get_alignments(
        args.audio_filepath,
        tokens,
        model,
        dictionary,
        args.use_star,
    )
    # Get spans of each line in input text file
    spans = get_spans(tokens, segments, stride)

    audio_id = os.path.basename(args.audio_filepath).split(".")[0]
    os.makedirs(args.output_dir, exist_ok=True)
    with open(f"{args.output_dir}/{audio_id}_manifest.jsonl", "w") as f:
        for i, t in enumerate(norm_transcripts):
            span = spans[i]
            seg_start_idx = span[0].start
            seg_end_idx = span[-1].end

            audio_start_sec = seg_start_idx * stride / 1000
            audio_end_sec = seg_end_idx * stride / 1000

            sample = {
                "audio_filepath": args.audio_filepath,
                "audio_start_sec": audio_start_sec,
                "duration": audio_end_sec - audio_start_sec,
                "text": transcripts[i],
            }
            f.write(json.dumps(sample) + "\n")

    return segments, stride


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Align and segment long audio files")
    parser.add_argument(
        "-a", "--audio-filepath", type=str, help="Path to input audio file"
    )
    parser.add_argument(
        "-t", "--text-filepath", type=str, help="Path to input text file "
    )
    parser.add_argument(
        "-l", "--lang", type=str, default="eng", help="ISO code of the language"
    )
    parser.add_argument(
        "-u", "--uroman-path", type=str, default="eng", help="Location to uroman/bin"
    )
    parser.add_argument(
        "-s",
        "--use-star",
        action="store_true",
        help="Use star at the start of transcript",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        help="Output directory to store segmented audio files",
    )
    print("Using torch version:", torch.__version__)
    print("Using torchaudio version:", torchaudio.__version__)
    print("Using device: ", DEVICE)
    args = parser.parse_args()
    main(args)
