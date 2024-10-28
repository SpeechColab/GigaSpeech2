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
Check language code in https://github.com/openai/whisper/blob/5979f03701209bb035a0a466f14131aeb1116cbb/whisper/tokenizer.py#L10-L111.

```shell
# Standard Whisper
python convert_and_transcribe.py
  --lang [whisper language code] \
  --root-dir [downloaded audio directory] \
  --save-dir [output directory]

# Faster Whisper
python convert_and_transcribe.py
  --lang [whisper language code] \
  --root-dir [downloaded audio directory] \
  --save-dir [output directory] \
  --use-faster-whisper True
```

For example:
```shell
# Standard Whisper
python convert_and_transcribe.py
  --lang zh \
  --root-dir ./download \
  --save-dir ./output_trans

# Faster Whisper
python convert_and_transcribe.py
  --lang zh \
  --root-dir ./download \
  --save-dir ./output_trans \
  --use-faster-whisper True
```
