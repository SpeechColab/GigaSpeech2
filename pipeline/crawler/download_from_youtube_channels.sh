#! /usr/bin/bash

echo "Language: $3"
echo "Read channels from file: $1, save to: $2"

lang=$3
log_dir=log

if [ ! -d $log_dir ]; then
  mkdir $log_dir
fi

while read rows
do
  echo "$rows"
  channel=`echo "$rows" | awk -F"\t" '{print $2}'`
  channel_name=`echo ${channel:1}`
  echo "Processing channel: $channel, channel name: $channel_name"
  yt-dlp -f 'ba' \
    --download-archive $log_dir/audios_$channel_name.txt \
    --sub-format vtt \
    --sub-langs $lang \
    https://www.youtube.com/${channel}/videos -o ${2}/$channel_name'/%(title).20s#%(channel_id)s#%(id)s_%(duration)s.%(ext)s' > $log_dir/$channel_name.log
done < $1
echo "Finished."

