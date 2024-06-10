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
  --input-dir ~/data/raw_alignment \
  --output-dir ~/data/alignment \
  --lid-model-path /tmp/lid.176.bin
```

### Segmentation the audio files
```shell
./segment.sh ~/data/alignment ~/data/clip
```
