import urllib.request
from PIL import Image
from time import sleep
import functions as f
import sys
import os


# Global Variables
CLIENT_ID = "CLIENT_ID"  # Spotify client token
CLIENT_SECRET = "CLIENT_SECRET"  # Spotify secret token
USERNAME = "USERNAME"  # User to login as
PLAYLISTID = "PLAYLISTID"  # ID of playlist to save songs to

REDIRECT_URI = "https://example.com/callback/"  # Site to redirect to when logged in
SCOPE = "user-read-currently-playing user-modify-playback-state playlist-modify-public"  # Permission levels for spotify

DURATION = 5  # Set duration of notifications
VERSION = "1.0.1"  # current version

#  Help file
usage = "\n" \
        "Usage:" \
        "   Spotipy <command>\n\n" \
        "Commands:\n" \
        "   prevsong            Skip User’s Playback To Previous Track\n" \
        "   playpause           Play/Pause a User's Playback\n" \
        "   nextsong            Skip User’s Playback To Next Track\n" \
        "   songsave            Save User’s Current Song To Playlist\n\n" \
        "General Options:\n" \
        "   -h                  Show this screen\n" \
        "   -v                  Show version and exit" \

# Sets True/False to toggle notifications/command line depending on os
if os.name == 'nt':
    noti = True
else:
    noti = False


def main():
    print("\nSpotipy %s" % VERSION)

    progs = ["songsave", "nextsong", "playpause", "prevsong", "songshow"]

    if len(sys.argv) == 2:
        if sys.argv[1] in progs:
            # get token & login to spotify
            token = f.get_token(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPE, USERNAME)
            if token:
                # login to spotify
                spotify = f.login(token)
                # get currently playing track of user
                current_track = spotify.current_user_playing_track()
                if current_track:
                    if sys.argv[1] == "songsave":
                        # print(current_track)
                        songsave(spotify, current_track)
                    elif sys.argv[1] == "nextsong":
                        nextsong(spotify)
                    elif sys.argv[1] == "prevsong":
                        prevsong(spotify)
                    elif sys.argv[1] == "playpause":
                        playpause(spotify, current_track)
                    elif sys.argv[1] == "songshow":
                        songshow(current_track)
                    else:
                        print("Argument not supported\n%s" % usage)
                else:
                    print("Currently no Spotify instance open")
            else:
                title = "Spotipy"
                message = "Oauth token request failed"
                f.notification(title, message, noti, DURATION)
        elif sys.argv[1] == "-h":
            print(usage)
        elif sys.argv[1] == "-v":
            print()
        else:
            print("Argument not supported\n%s" % usage)
    elif len(sys.argv) > 2:
        print("Only supports one argument\n%s" % usage)
    elif len(sys.argv) == 1:
        print("Requires an argument below\n%s" % usage)


def nextsong(spotify):
    # next track
    spotify.next_track()
    print("Next Song...")


def prevsong(spotify):
    # previous track
    spotify.previous_track()
    print("Previous Song...")


def playpause(spotify, current_track):
    is_playing = f.DictQuery(current_track).get("is_playing")

    if is_playing:
        spotify.pause_playback()
        print("Playback Paused...")
    else:
        spotify.start_playback()
        print("Playback Resumed...")


def songsave(spotify, current_track):
    is_playing = f.DictQuery(current_track).get("is_playing")

    if is_playing:
        # get current track uri
        current_track_uri = [f.DictQuery(current_track).get("item/id")]  # current playing uri

        user = spotify.current_user()  # get logged in user as dict
        userid = f.DictQuery(user).get("id")  # logged in user id/username

        # get playlist info as dict
        playlist = spotify.user_playlist(user=userid, playlist_id=PLAYLISTID, fields="name,tracks")

        # gets playlist name for output
        plistname = playlist["name"]

        # gets ids of tracks in playlist into list
        playlist_tracks = playlist['tracks']
        playlist_tracks_id = []
        for item in playlist_tracks['items']:
            playlist_tracks_id.append(item['track']['id'])

        # adds currently playing to playlist
        if current_track_uri[0] in playlist_tracks_id:
            title = "Spotipy"
            message = "Track already in playlist"
            f.notification(title, message, noti, DURATION)
        else:
            # adds track to playlist
            spotify.user_playlist_add_tracks(user=userid, playlist_id=PLAYLISTID, tracks=current_track_uri)
            # show notification
            title = "Spotipy - Track saved to '%s'" % plistname
            songshow_func(current_track, title)
    else:
        title = "Spotipy"
        message = "Spotify currently paused"
        f.notification(title, message, noti, DURATION)


def songshow(current_track):
    title = "Spotipy - Current track properties"
    songshow_func(current_track, title)


def songshow_func(current_track, title):
    is_playing = f.DictQuery(current_track).get("is_playing")

    if is_playing:
        # get current track properties
        song = f.DictQuery(current_track).get("item/name")
        artist = f.DictQuery(current_track).get("item/artists/name")[0]
        album = f.DictQuery(current_track).get("item/album/name")

        # get image for noti
        rartist = f.remove(artist, '\/:*?"<>|')
        ralbum = f.remove(album, '\/:*?"<>|')

        pngpath = "images\\%s - %s.png" % (rartist, ralbum)  # where to save .png
        icopath = "images\\%s - %s.ico" % (rartist, ralbum)  # where to save .ico
        if noti:
            imageurl = f.DictQuery(current_track).get("item/album/images/url")[2]  # get album image url
            urllib.request.urlretrieve(imageurl, pngpath)  # download image
            ico_file = Image.open(pngpath)  # open png as PIL Image object
            ico_file.save(icopath, sizes=[(64, 64)])  # convert ong to ico and save

        # show notification
        message = "Song: %s \nArtist: %s\nAlbum: %s" % (song, artist, album)
        f.notification(title, message, noti, DURATION, image=icopath)

        if noti:
            # delete saved images
            sleep(DURATION)
            f.delete(pngpath)
            f.delete(icopath)

    else:
        title = "Spotipy"
        message = "Spotify currently paused"
        f.notification(title, message, noti, DURATION)


if __name__ == "__main__":
    main()
