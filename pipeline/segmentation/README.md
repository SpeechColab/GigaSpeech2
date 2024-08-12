## Usage
### Installation
```shell
pip install fasttext
```

### Download the language identification model
```shell
wget -P /tmp https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
```

### Modify the filtering rules
```shell
vim filter_manifest.py
```

### Filter the segments
```shell
python filter_manifest.py \
  --input-dir [forced-aligned manifests directory] \
  --output-dir [output directory] \
  --lid-model-path [path to lid.176.bin]
```

### Segmentation the audio files
```shell
./segment.sh [filtered manifests directory] [output directory]
```
