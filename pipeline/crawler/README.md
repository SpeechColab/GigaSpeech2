## Installation
```shell
pip install git+https://github.com/yt-dlp/yt-dlp.git
```

## Usage
### Create a list of youtube channels
You need to create a list of YouTube channel names from which you intend to download audio. Save this list in a text file (e.g., `th_channels.txt`) using the format `[channel name]\t@[channel id]`.

For example:
```
Thairath Online  @thairathonline
Thai PBS News  @ThaiPBSNews
```

### Start the download process
```
./download_from_youtube_channels.sh channels.txt ~/download
```
