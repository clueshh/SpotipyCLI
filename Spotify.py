import spotipy


class Spotify:
    def __init__(self, client_id, client_secret, username, playlist_id):
        self.__CLIENT_ID = client_id  # Spotify client token
        self.__CLIENT_SECRET = client_secret  # Spotify secret token
        self.__USERNAME = username  # User to login as
        self.__PLAYLISTID = playlist_id  # ID of playlist to save songs to

        # Site to redirect to when logged in
        self.__REDIRECT_URI = "https://example.com/callback/"

        # Permission levels for spotify
        self.__SCOPE = "user-read-currently-playing " \
                       "user-modify-playback-state " \
                       "playlist-modify-public"

        self.spotify = self.__login()
        print(f"Successfully logged in as {self.__USERNAME}")

    def __str__(self) -> str:
        return super().__str__()

    def __get_token(self):
        return spotipy.util.prompt_for_user_token(username=self.__USERNAME,
                                                  scope=self.__SCOPE,
                                                  client_id=self.__CLIENT_ID,
                                                  client_secret=self.__CLIENT_SECRET,
                                                  redirect_uri=self.__REDIRECT_URI)

    def __login(self):
        return spotipy.Spotify(auth=self.__get_token())

    def __current_playing_track(self):
        current_track = self.spotify.current_user_playing_track()
        if current_track:
            return current_track
        else:
            print("Spotify Currently Paused")
            return None

    def __current_playing_track_uri(self):
        return self.__DictQuery(self.__current_playing_track()).get("item/id")[0]

    def __is_playing(self):
        is_playing = self.__DictQuery(self.__current_playing_track()) \
            .get("is_playing")

        if is_playing:
            return is_playing
        else:
            print("Spotify Currently Paused")
            return None

    def nextsong(self):
        # next track
        self.spotify.next_track()
        print("Next Song...")

    def prevsong(self):
        # previous track
        self.spotify.previous_track()
        print("Previous Song...")

    def playpause(self):
        if self.__current_playing_track():

            if self.__is_playing():
                self.spotify.pause_playback()
                print("Playback Paused...")
            else:
                self.spotify.start_playback()
                print("Playback Resumed...")

    def songsave(self):
        if self.__is_playing():
            # get current track uri
            current_track_uri = self.__current_playing_track_uri()

            # get playlist info as dict
            playlist = self.spotify.playlist(playlist_id=self.__PLAYLISTID, fields="name,tracks")

            # gets ids of tracks in playlist into list
            playlist_tracks = playlist['tracks']
            playlist_tracks_id = []
            for item in playlist_tracks['items']:
                playlist_tracks_id.append(item['track']['id'])

            # adds currently playing to playlist
            if current_track_uri not in playlist_tracks_id:
                # adds track to playlist
                self.spotify.user_playlist_add_tracks(
                    user=self.__USERNAME,
                    playlist_id=self.__PLAYLISTID,
                    tracks=current_track_uri)

    class __DictQuery(dict):
        def get(self, path, default=None):
            keys = path.split("/")
            val = None

            for key in keys:
                if val:
                    if isinstance(val, list):
                        val = [v.get(key, default) if v else None for v in val]
                    else:
                        val = val.get(key, default)
                else:
                    val = dict.get(self, key, default)
                if not val:
                    break
            return val
