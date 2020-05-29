import sys
from configparser import ConfigParser
from Spotify import Spotify

config = ConfigParser()
config.read('credentials.ini')

CLIENT_ID = config.get("DEFAULT", "CLIENT_ID")  # Spotify client token
CLIENT_SECRET = config.get("DEFAULT", "CLIENT_SECRET")  # Spotify secret token
USERNAME = config.get("DEFAULT", "USERNAME")  # User to login as
PLAYLISTID = config.get("DEFAULT", "PLAYLIST_ID")  # ID of playlist to save songs to

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
        "   -v                  Show version and exit"

if __name__ == "__main__":
    print("\nSpotipy %s" % VERSION)

    progs = ["songsave", "nextsong", "playpause", "prevsong"]

    if len(sys.argv) == 2:
        if sys.argv[1] in progs:
            s = Spotify(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, username=USERNAME, playlist_id=PLAYLISTID)
            if sys.argv[1] == "songsave":
                s.songsave()
            elif sys.argv[1] == "nextsong":
                s.nextsong()
            elif sys.argv[1] == "prevsong":
                s.prevsong()
            elif sys.argv[1] == "playpause":
                s.playpause()
            else:
                print("Argument not supported\n%s" % usage)
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
