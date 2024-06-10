#! /usr/bin/bash

corpus_dir=${2%/}
output_dir=${3%/}
lang=$4

while IFS= read -r wav; do
  id=$(basename "${wav}" .wav)
  echo "Process $id"
  text="${corpus_dir}/${id}.txt"

  python ../utils/force_alignment/align.py \
    -a $wav \
    -t $text \
    --lang $lang \
    --output-dir $output_dir \
    --uroman ../utils/uroman/bin
done < $1
