## Usage
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
  --input-dir [corpus directory] \
  --output-dir [output directory] \
  --lid-model-path [path to lid.176.bin]
```

### Segmentation the audio files
Note that the `filtered corpus directory` is the output of `filter_manifest.py`.
```shell
./segment.sh [filtered corpus directory] [output directory]
```
