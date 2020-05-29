# SpotipyCLI

[Spotipy](https://github.com/plamere/spotipy) command line interface to interact with spotify.

## Toolbar

To use as a toolbar create a folder and add a windows lnk file that points to

```bash
C:\path\to\Python\Python37\pythonw.exe "C:\users\username\SpotipyCLI\SpotipyCLI.py" prevsong
```

![alt text](toolbar.png)

## Requirements

```sh
pip install requirements.txt
```

Create a file `credentials.ini` with the following lines and update with your api keys & spotify login

```ini
[DEFAULT]
CLIENT_ID = CLIENT_ID  # Spotify client token
CLIENT_SECRET = CLIENT_SECRET  # Spotify secret token
USERNAME = USERNAME  # User to login as
PLAYLISTID = PLAYLISTID  # ID of playlist to save songs to
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
