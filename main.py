import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ["SPOTIFY_ID"]
CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
REDIRECT_ID = "https://open.spotify.com/"


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_ID,
        scope="playlist-modify-private playlist-modify-public",
        cache_path="token.txt"
    )
)
user = sp.current_user()
user_id = user["id"]


song_title_list = []
song_uris = []

def get_billboard_list():

    url = requests.get('https://www.billboard.com/charts/year-end/2025/billboard-global-200/')
    soup = BeautifulSoup(url.content, 'html.parser')
    all_songs = soup.find_all("div", class_="chart-results-list")

    for songs in all_songs:
        song_title = songs.find_all('h3', class_="c-title", id='title-of-a-story')

        for title in song_title:
            song = title.get_text(strip=True)
            song_title_list.append(song)


def get_song_uri():
    year = 2025

    for song in my_list:
        result = sp.search(q=f"track:{song} year:{year}", type="track")
        try:
            uri = result["tracks"]["items"][0]["uri"]
            song_uris.append(uri)
        except IndexError:
            print(f"{song} doesn't exist in Spotify. Skipped.")



get_billboard_list()
my_list = song_title_list [:100]
get_song_uri()


# Create Playlist
playlist = sp.user_playlist_create(
    user=user_id,
    name="Top 100 Billboard songs",
    public=False,
    collaborative=False,
    description="Top 100 Billboard songs of 2025",
)

playlist_id = playlist["id"]

# Add song to playlist
sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)
