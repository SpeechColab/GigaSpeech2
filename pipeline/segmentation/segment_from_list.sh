#! /usr/bin/bash
output_dir=${2%/}

while IFS= read -r manifest; do
  id=$(basename "${manifest}" .jsonl)
  echo "Process $id"

  python segment_from_manifests.py \
    -m $manifest \
    -o $output_dir
done < $1
