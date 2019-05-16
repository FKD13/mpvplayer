# mpvplayer

## requirements

 - obviously **Python 3**
 - [mpv](https://mpv.io/)
 - [youtube-dl](https://ytdl-org.github.io/youtube-dl/index.html)
 - [python-mpv](https://github.com/jaseg/python-mpv)
 - [pafy](https://pypi.org/project/pafy/)

## features

 - when a song ends the program will play the next song in the playlist
 
## commands

 - `> find <search item>` returns a list of youtube video's matching the search item.
 - `> add <search item id>` add the video with selected id to playlist.
 - `> addall` add all search items to the playlist.
 - `> play` play the next song in the playlist.
 - `> play <id>` play the element in the playlist with id = <id>.
 - `> skip` play the next song in the playlist.
 - `> skip <nr>` skip <nr> numbers.
 - `> list` returns the playlist.
 - `> quit` close the program and video.
