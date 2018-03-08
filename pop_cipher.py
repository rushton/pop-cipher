from argparse import ArgumentParser
import json
from random import shuffle

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys

def generate_cipher_text(input_text, songs):
    cipher = []
    for char in input_text:
        if char == ' ': continue
        shuffle(songs)
        song = None
        while not song and song not in cipher:
            song = find_song(char, songs)
            if song not in cipher:
                cipher.append(song)
    return cipher

def find_song(char, songs):
    for song in songs:
        for idx, song_char in enumerate(song.get('artist')):
            if song_char.lower() == char.lower():
                return {'song': song, 'index': idx}
def main():
    parser = ArgumentParser(description="Create cipher using pop music")
    parser.add_argument("input_text", type=str)
    parser.add_argument("--songs_json_file", type=str, default="data.json")
    parser.add_argument("--spotify-client-id", type=str, default=None)
    parser.add_argument("--spotify-client-secret", type=str, default=None)
    args = parser.parse_args()

    client_credentials_manager = SpotifyClientCredentials(args.spotify_client_id, args.spotify_client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    with open(args.songs_json_file) as fp:
        cipher = generate_cipher_text(args.input_text, json.load(fp))
        for char in cipher:
            artist = char.get('song').get('artist')
            title = char.get('song').get('title')
            sys.stderr.write(artist + " " + str(char.get('index')) + "\n")
            for preview_url in [x.get('preview_url') for x in sp.search(q=title, limit=10)['tracks']['items']]:
                if preview_url:
                    print(preview_url + " " + str(char.get('index')))
                    break

if __name__ == '__main__':
    main()
