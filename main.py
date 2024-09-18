import requests
import spotipy
from datetime import datetime
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup


ID="45b19d163c9840e3b424cf2ba655f113"
SECRET="6276f8b0e57640ef8bac531d4bcecb99"
Redirect_Url="http://example.com"

n=input("Which Year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

url=f"https://www.billboard.com/charts/hot-100/{n}/"

response=requests.get(url=url)
html_code=response.text

soup=BeautifulSoup(html_code,"html.parser")

song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]
print(song_names)



sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id=ID, client_secret=SECRET, redirect_uri=Redirect_Url,scope="playlist-modify-private")

access_token = sp_oauth.get_access_token()

with open ("token.text","w")as file:
    file.write(str(access_token))

import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=Redirect_Url,
        client_id=ID,
        client_secret=SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username="Sangusaishanmukha",
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = n.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{n} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)