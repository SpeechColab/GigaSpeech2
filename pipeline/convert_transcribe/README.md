## Installation
```shell
conda install ffmpeg
pip install ffmpeg-python
```

### Option 1: Standard Whisper

```shell
pip install git+https://github.com/openai/whisper.git
```

### Option 2: Faster whisper

```shell
pip install faster-whisper
```

## Usage

```shell
# Standard Whisper
python convert_and_transcribe.py
  --lang [ISO 639-1 language code] \
  --root-dir [downloaded audio directory] \
  --save-dir [output directory]

# Faster Whisper
python convert_and_transcribe.py
  --lang [ISO 639-1 language code] \
  --root-dir [downloaded audio directory] \
  --save-dir [output directory] \
  --use-faster-whisper True
```
