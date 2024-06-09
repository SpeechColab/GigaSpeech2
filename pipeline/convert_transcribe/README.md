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
  --lang th \
  --root-dir ~/download \
  --save-dir ~/data

# Faster whisper
python convert_and_transcribe.py
  --lang th \
  --root-dir ~/download \
  --save-dir ~/data \
  --use-faster-whisper True
```