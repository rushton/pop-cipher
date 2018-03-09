from argparse import ArgumentParser
import json
from random import shuffle

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
from sys import stderr

MAX_SONG_SEARCH_ATTEMPTS = 5
def generate_cipher(input_text, songs, banlist):
    cipher = []
    selected_songs = []
    banned = False

    for char in input_text:
        if char == ' ': continue
        song = None
        search_attempt_count = 0

        while not song:
            shuffle(songs)
            song = find_song(char, songs)
            artist = song.get('song').get('artist')

            for nope in banlist:
                if nope.lower() in artist.lower():
                    sys.stderr.write("Ew, " + artist + "\n")
                    banned = True # get new song

            if not banned and artist + song.get('song').get('title') not in selected_songs:
                cipher.append(song)
                selected_songs.append(song.get('song').get('artist') + song.get('song').get('title'))
            else:
                song = None

            search_attempt_count += 1
            if search_attempt_count > MAX_SONG_SEARCH_ATTEMPTS:
                sys.stderr.write("Not enough songs for cipher \n")
                sys.exit()

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
    parser.add_argument("--banlist", nargs='+', default=[])
    args = parser.parse_args()

    client_credentials_manager = SpotifyClientCredentials(args.spotify_client_id, args.spotify_client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    with open(args.songs_json_file) as fp:
        banlist = args.banlist
        if banlist == ["none"]:
            banlist = []

        cipher = generate_cipher(args.input_text, json.load(fp), banlist)
        for char in cipher:
            artist = char.get('song').get('artist')
            title = char.get('song').get('title')
            for preview_url in [x.get('preview_url') for x in sp.search(q=artist + " " + title, limit=10)['tracks']['items']]:
                if preview_url:
                    print(preview_url + " " + str(char.get('index') + 1))
                    break

if __name__ == '__main__':
    main()
