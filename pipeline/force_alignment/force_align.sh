#! /usr/bin/bash
corpus_dir=${1%/}
output_dir=${2%/}
lang=$3

for text in ${corpus_dir}/*.txt; do
  id=$(basename "${text}" .txt)
  echo "Process $id"
  wav="${corpus_dir}/${id}.wav"

  python ../../utils/force_alignment/align.py \
    -a $wav \
    -t $text \
    --lang $lang \
    --output-dir $output_dir \
    --uroman ../../uroman/bin
done
