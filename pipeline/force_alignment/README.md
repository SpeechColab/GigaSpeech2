## Installation
```shell
git submodule update --init --recursive
pip install torchaudio==2.1.0  # >= 2.1.0
pip install sox 
pip install dataclasses 
```

## Usage
You need to specify the [ISO 639-2 language code](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes).
```shell
./force_align.sh [corpus directory] [output directory] [ISO 639-2 language code]
```

For example:
```shell
./force_align.sh ./data ./output zho
```
