# SpotipyCLI

Spotipy command line program to use as a toolbar

![alt text](toolbar.png)

In the toolbar directory add a windows lnk file that points to

```bash
C:\path\to\Python\Python37\pythonw.exe "C:\users\username\SpotipyCLI\main.pyw" prevsong
```

## Requirements

```sh
pip install requirements.txt
```

update the following lines with your api keys & spotify login

```python
CLIENT_ID = "CLIENT_ID"  # Spotify client token
CLIENT_SECRET = "CLIENT_SECRET"  # Spotify secret token
USERNAME = "USERNAME"  # User to login as
PLAYLISTID = "PLAYLISTID"  # ID of playlist to save songs to
```

## Arguments

| command       | function                               |
| ------------- |:---------------------------------------|
| prevsong      | Skip User’s Playback To Previous Track |
| playpause     | Play/Pause a User's Playback           |
| nextsong      | Skip User’s Playback To Next Track     |
| songsave      | Save User’s Current Song To Playlist   |
| -h            | Show this screen                       |
| -v            | Show version and exit                  |
