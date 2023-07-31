import json
import sys

import spotipy
import spotipy.util as util

from .Toolkit import Tool, Toolkit

# -------------------------------
# SETUP
# -------------------------------

scope = "user-modify-playback-state user-read-playback-state"
username = "eholter27"

token = util.prompt_for_user_token(username, scope)
if not token:
    raise (Exception, "Auth token is invalid")

sp = spotipy.Spotify(auth=token)

# -------------------------------
# FUNCTIONS
# -------------------------------

def get_current_song():
    response = sp.current_playback(additional_types="episode")
    media_type = response.get("currently_playing_type")
    
    if media_type == "track":
        result = {
            "media_type": "song",
            "song": response.get("item").get("name"),
            "artist": response.get("item").get("artists")[0].get("name"),
            "album": response.get("item").get("album").get("name")
        }
    
    if media_type == "episode":
        result = {
            "media_type": response.get("item").get("type"),
            "name": response.get("item").get("name"),
            "publisher":  response.get("item").get("publisher")
        }
    
    if media_type == "ad":
        result = {
            "media_type": "advertisement"
        }
    
    if media_type == "unknown":
        result = {
            "media_type": "unknown"
        }
    
    if not result:
        raise(ValueError, "Invalid media type")
    
    return json.dumps(result)

# -------------------------------
# TOOLKIT SETUP
# -------------------------------

spotify_toolkit = Toolkit()
spotify_toolkit.setTools(
    [
        Tool(
            name="pause_music",
            description="pauses the spotify music",
            callback=sp.pause_playback,
            required=[],
            properties={},
        ),
        Tool(
            name="resume_music",
            description="resumes the spotify music",
            callback=sp.start_playback,
            required=[],
            properties={},
        ),
        Tool(
            name="get_current_song",
            description="get the song, album, and artist name of the current song",
            callback=get_current_song,
            required=[],
            properties={}
        )
    ]
)