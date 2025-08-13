# spotify.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# from dotenv import load_dotenv
# import os

# load_dotenv()

scope = "user-library-read user-read-recently-played user-top-read user-read-playback-state"

def get_user_display_name(sp):
    user = sp.current_user()
    return user.get('display_name', user.get('id', 'Unknown'))

def get_spotify_client():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id='7fdb4c0a195d46d9b08957804073a228',
        client_secret='a5fb4cd3b9e74c708e7d51a30a34a6a2',
        redirect_uri='http://127.0.0.1:8888/callback',
        scope=scope
    ))
    return sp

def get_recent_tracks(sp):
    try:
        results = sp.current_user_recently_played(limit=50)
        items = results.get('items', [])
        if items:
            tracks = []
            for item in items:
                track = item['track']
                name = track['name']
                artist = track['artists'][0]['name']
                album = track['album']['name']
                # Get the largest image if available
                images = track['album'].get('images', [])
                image_url = images[0]['url'] if images else None
                external_url = track.get('external_urls', {}).get('spotify')
                tracks.append({
                    'name': name,
                    'artist': artist,
                    'album': album,
                    'image_url': image_url,
                    'spotify_url': external_url
                })
            return tracks
        else:
            return get_top_tracks(sp)
    except Exception as e:
        print(f"Error fetching recent tracks: {e}")
        return get_top_tracks(sp)

def get_top_tracks(sp):
    try:
        results = sp.current_user_top_tracks(limit=50, time_range='short_term')
        items = results.get('items', [])
        tracks = []
        for item in items:
            name = item['name']
            artist = item['artists'][0]['name']
            album = item['album']['name']
            images = item['album'].get('images', [])
            image_url = images[0]['url'] if images else None
            external_url = item.get('external_urls', {}).get('spotify')
            tracks.append({
                'name': name,
                'artist': artist,
                'album': album,
                'image_url': image_url,
                'spotify_url': external_url
            })
        return tracks
    except Exception as e:
        print(f"Error fetching top tracks: {e}")
        return []
