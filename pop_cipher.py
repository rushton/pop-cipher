from argparse import ArgumentParser
import json
from random import shuffle

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys

def generate_cipher(input_text, songs):
    cipher = []
    selected_songs = []
    for char in input_text:
        if char == ' ': continue
        song = None
        while not song:
            shuffle(songs)
            song = find_song(char, songs)
            if song.get('song').get('artist') + song.get('song').get('title') not in selected_songs:
                cipher.append(song)
                selected_songs.append(song.get('song').get('artist') + song.get('song').get('title'))
            else:
                song = None
    return cipher

def find_song(char, songs):
    for song in songs:
        for idx, song_char in enumerate(song.get('artist')):
            if song_char.lower() == char.lower():
                return {'song': song, 'index': idx}
def main():
    parser = ArgumentParser(description="Create cipher using pop music")
    parser.add_argument("input_text", type=str)
    parser.add_argument("--songs-json-file", type=str, default="data.json")
    parser.add_argument("--spotify-client-id", type=str, default=None)
    parser.add_argument("--spotify-client-secret", type=str, default=None)
    args = parser.parse_args()

    client_credentials_manager = SpotifyClientCredentials(args.spotify_client_id, args.spotify_client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    with open(args.songs_json_file) as fp:
        cipher = generate_cipher(args.input_text, json.load(fp))
        for char in cipher:
            artist = char.get('song').get('artist')
            title = char.get('song').get('title')
            for preview_url in [x.get('preview_url') for x in sp.search(q=artist + " " + title, limit=10)['tracks']['items']]:
                if preview_url:
                    print(preview_url + " " + str(char.get('index') + 1))
                    break

if __name__ == '__main__':
    main()
