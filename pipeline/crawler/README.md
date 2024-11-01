## Installation
```shell
pip install git+https://github.com/yt-dlp/yt-dlp.git
```

## Usage
### Create a list of youtube channels
You need to create a list of YouTube channel names from which you intend to download audio. Save this list in a text file (e.g., `zh_channels.txt`) using the format `[channel name]\t@[channel id]`.

For example:
```
Youth With You  @iQIYIYouthWithYou
KUN  @kun_global
Kun's Official Channel  @kunsofficialchannel6831
```

### Start the download process
```shell
./download_from_youtube_channels.sh [channels list file] [download directory]
```

For example:
```shell
./download_from_youtube_channels.sh zh_channels.txt ./download
```
