#! /usr/bin/bash

corpus_dir=${2%/}
output_dir=${3%/}
lang=$4

while IFS= read -r text; do
  id=$(basename "${text}" .txt)
  echo "Process $id"
  wav="${corpus_dir}/${id}.wav"

  python ../utils/force_alignment/align.py \
    -a $wav \
    -t $text \
    --lang $lang \
    --output-dir $output_dir \
    --uroman ../utils/uroman/bin
done < $1
