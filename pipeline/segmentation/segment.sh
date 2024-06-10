#! /usr/bin/bash

manifest_dir=${1%/}
output_dir=${2%/}

for manifest in ${manifest_dir}/*.jsonl; do
  id=$(basename "${manifest}" .jsonl)
  echo "Process $id"

  python segment_from_manifests.py \
    -m $manifest \
    -o $output_dir
done
