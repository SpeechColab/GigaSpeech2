import argparse
import os
import shutil
import struct
import subprocess
from concurrent.futures import ProcessPoolExecutor
from functools import partial

from tqdm import tqdm


def read_wav_info(filename):
    with open(filename, "rb") as wav_file:
        a = wav_file.read(28)
    sr = struct.unpack("i", a[24:28])[0]
    channel = struct.unpack("h", a[22:24])[0]
    length = (struct.unpack("i", a[4:8])[0] - 70) / channel / 2 / sr
    return sr, length


def ffmpeg_convert(file_from, file_to):
    try:
        subprocess.call(
            [
                "ffmpeg",
                "-loglevel",
                "warning",
                "-y",
                "-i",
                file_from,
                "-ac",
                "1",
                "-ar",
                "16000",
                "-acodec",
                "pcm_s16le",
                file_to,
            ]
        )
    except Exception as e:
        print(file_to, e)
    return


def video2wav(args):
    video_format = {".mov", ".avi", ".flv", ".ogg", ".mp4", ".mkv", "webm"}
    if not os.path.exists(args.wav_dir):
        os.makedirs(args.wav_dir, exist_ok=True)

    # Start multiprocess
    executor = ProcessPoolExecutor(max_workers=args.workers)
    print(f"> Using {args.workers} workers!")
    futures = []
    files = os.listdir(args.root_dir)
    files = set([x for x in files if x[-4:] in video_format])
    print("Total videos to convert: ", len(files))

    for file_name in files:
        file_raw = os.path.join(args.root_dir, file_name)
        file_to = os.path.join(
            args.wav_dir, file_name.split(".")[-2][-11:] + args.format
        )
        if os.path.exists(file_to):
            continue
        futures.append(executor.submit(partial(ffmpeg_convert, file_raw, file_to)))

    result_list = [future.result() for future in tqdm(futures)]
    print(len(result_list), "wavs resampled.")


def wav2whisper(args):
    # remove exsit files
    wav_dir = (
        os.path.join(args.wav_dir, args.section)
        if args.section is not None
        else args.wav_dir
    )
    wavs = os.listdir(wav_dir)
    exist_files = set([x.split(".")[0] for x in os.listdir(args.sub_dir)])
    error_files = os.path.join(args.list_dir, "error_files.txt")
    if os.path.exists(error_files):
        lines = set(open(error_files, "r", encoding="utf-8").readlines())
        open(error_files, "w", encoding="utf-8").write("".join(list(lines)))
        lines = set(x.strip().split("/")[-1][:-4] for x in lines)
        print(
            "Recognized: ",
            len(exist_files),
            "Language mismatched:",
            len(lines),
            "Total skip:",
            len(exist_files | lines),
        )
        exist_files |= lines
    wavs = [x for x in wavs if x.split(".")[0] not in exist_files]

    if args.use_faster_whisper:
        from faster_whisper import WhisperModel

        model = WhisperModel(args.model_size, device="cuda", compute_type="float16")
        for wav in tqdm(wavs):
            audio_path = os.path.join(wav_dir, wav)
            segments, info = model.transcribe(audio_path, language=lang, beam_size=5)
            if info.language != args.lang:
                print(f"Expect {args.lang} Detected: {info.language} {audio_path}")
                with open(error_files, "a") as f:
                    f.write(
                        f"Expect {args.lang} Detected: {info.language} {audio_path}\n"
                    )
                continue
            result_path = os.path.join(args.sub_dir, wav.replace("wav", "txt"))
            with open(result_path, "w") as f:
                for segment in segments:
                    f.write(segment.text + "\n")
    else:
        import whisper
        from whisper.utils import get_writer

        def detect_language(audio_path):
            # load audio and pad/trim it to fit 30 seconds (start from middle part)
            audio = whisper.load_audio(audio_path)
            audio = audio[int(len(audio) / 2) :]
            audio = whisper.pad_or_trim(audio)

            # make log-Mel spectrogram and move to the same device as the model
            mel = whisper.log_mel_spectrogram(audio, n_mels=n_mels).to(model.device)

            # detect the spoken language
            _, probs = model.detect_language(mel)
            return max(probs, key=probs.get)

        model = whisper.load_model(args.model_size)
        n_mels = 128 if "large" in args.model_size else 80
        writer = get_writer("txt", args.sub_dir)
        for wav in tqdm(wavs):
            audio_path = os.path.join(wav_dir, wav)
            lang = detect_language(audio_path)
            if lang != args.lang:
                print(f"Expect {args.lang} Detected: {lang} {audio_path}")
                with open(error_files, "a", encoding="utf-8") as f:
                    f.write(f"Expect {args.lang} Detected: {lang} {audio_path}\n")
                continue
            subtitle = model.transcribe(audio_path, language=lang, beam_size=5)
            writer(subtitle, audio_path)


def construct_corpus(args):
    wav_dir = (
        os.path.join(args.wav_dir, args.section)
        if args.section is not None
        else args.wav_dir
    )
    wavs = os.listdir(wav_dir)
    wavs = set([x.split(".")[0] for x in wavs if x[-3:] == "wav"])
    txts = os.listdir(args.sub_dir)
    txts = set([x.split(".")[0] for x in txts if x[-3:] == "txt"])
    corpus = os.listdir(args.corpus_dir)
    corpus = set([x.split(".")[0] for x in corpus])
    move_list = wavs & txts

    for x in move_list:
        if x in corpus:
            continue
        try:
            read_wav_info(os.path.join(wav_dir, x + ".wav"))
        except Exception as e:
            print(x + ".wav", e)
            continue
        shutil.move(
            os.path.join(wav_dir, x + ".wav"), os.path.join(args.corpus_dir, x + ".wav")
        )
        shutil.move(
            os.path.join(args.sub_dir, x + ".txt"),
            os.path.join(args.corpus_dir, x + ".txt"),
        )
    print("Total files in corpus:", len(os.listdir(args.corpus_dir)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--lang",
        type=str,
        help="See ISO 639-1 codes for supported languages (total: 97).",
    )
    parser.add_argument(
        "--format",
        type=str,
        default=".wav",
        help="Set audio format, find other options in ffmpeg documentation.",
    )
    parser.add_argument(
        "--list-dir", type=str, default="./list", help="Path to save channel lists."
    )
    parser.add_argument(
        "--root-dir",
        type=str,
        default="./download",
        help="Dictionary path of downloaded videos.",
    )
    parser.add_argument(
        "--save-dir",
        type=str,
        default="./data",
        help="Dictionary path to save audio files.",
    )
    parser.add_argument(
        "--section", type=str, default=None, help="Section to transribe."
    )
    parser.add_argument(
        "--model-size",
        type=str,
        default="large-v3",
        help="Whisper model size (large, medium, small, base, tiny)",
    )
    parser.add_argument(
        "--use-faster-whisper",
        type=bool,
        default=False,
        help="Whether to use faster-whisper",
    )
    parser.add_argument("--workers", type=int, default=16, help="Multiprocess workers.")
    args = parser.parse_args()

    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir, exist_ok=True)
    args.sub_dir = os.path.join(args.save_dir, "whisper")
    args.wav_dir = os.path.join(args.save_dir, "audios")
    args.corpus_dir = os.path.join(args.save_dir, "corpus")
    os.makedirs(args.sub_dir, exist_ok=True)
    os.makedirs(args.wav_dir, exist_ok=True)
    os.makedirs(args.corpus_dir, exist_ok=True)

    # convert video to wav
    video2wav(args)

    # process subtitle and video info
    wav2whisper(args)

    # Pair wav and txt file
    construct_corpus(args)


if __name__ == "__main__":
    main()
