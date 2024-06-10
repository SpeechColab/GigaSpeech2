## Installation
```shell
wget -P /tmp https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
```

## Usage
```shell
# Filter
python filter_manifest.py \
  --input-dir ~/data/raw_alignment \
  --output-dir ~/data/alignment \
  --lid-model-path /tmp/lid.176.bin

# Segmentation
./segment.sh ~/data/alignment ~/data/clip
```
