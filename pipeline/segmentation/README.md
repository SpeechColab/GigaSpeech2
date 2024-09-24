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

For example:
```shell
python filter_manifest.py \
  --input-dir ./output_force_align \
  --output-dir ./output_filter \
  --lid-model-path ./lid.176.bin
```

### Segmentation the audio files
```shell
./segment.sh [filtered manifests directory] [output directory]
```

For example:
```shell
./segment.sh ./output_filter ./output_segment
```
