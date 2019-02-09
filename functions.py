#! /usr/bin/env python
import os
from win10toast import ToastNotifier
import spotipy.util as util
import spotipy


def notification(title, message, noti, duration, image="icons\\2000px-Spotify_logo.ico"):
    if noti:
        toaster = ToastNotifier()
        toaster.show_toast(title,
                           message,
                           icon_path=image,
                           duration=duration,
                           threaded=True)
    else:
        print(title + '\n' + message)


def remove(value, deletechars):
    for c in deletechars:
        value = value.replace(c, '_')
    return value


def get_token(client_id, client_secret, redirect_uri, scope, username):
    return util.prompt_for_user_token(username=username,
                                      scope=scope,
                                      client_id=client_id,
                                      client_secret=client_secret,
                                      redirect_uri=redirect_uri)


def login(token):
    # login to spotify
    spotify = spotipy.Spotify(auth=token)

    # get username and print
    sid = DictQuery(spotify.current_user()).get("id")
    print("Successfully logged in as %s\n" % sid)

    return spotify


def delete(path):
    if os.path.isfile(path):
        try:
            os.remove(path)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
    else:
        print("Error: %s file not found" % path)


class DictQuery(dict):
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
