from argparse import ArgumentParser
import json
from random import shuffle

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
from sys import stderr

MAX_SONG_SEARCH_ATTEMPTS = 5


class PopCipher(object):
    """
        class for encrypting text using pop cipher
    """
    def __init__(self, songs, banlist):
        """
            Args:
                songs - list[dict] of [{'title': <str>, 'artist': <str>}, ...]
                banlist - list[str] - list of banned artists
        """
        self.songs = [s for s in songs if s.get('artist').lower() not in banlist]

    def encrypt(self, input_text):
        """
            Args:
                input_text - str
            Return:
                list[dict] - [{'song': {'title', <str>, 'artist': <str>}, 'index': <int>}, ...]
        """
        output = []
        low_pri_songs = []

        for char in input_text:
            if char == ' ':
                continue
            song = None
            search_attempt_count = 0

            while not song:
                shuffle(self.songs)
                shuffle(low_pri_songs)
                high_pri_songs = [s for s in self.songs if s not in low_pri_songs]
                song = self.find_song(char, high_pri_songs) or self.find_song(char, low_pri_songs)

                if song:
                    output.append(song)
                    if song not in low_pri_songs:
                        low_pri_songs.append(song)

                search_attempt_count += 1
                if search_attempt_count > MAX_SONG_SEARCH_ATTEMPTS:
                    stderr.write("Not enough songs to encrypt \n")
                    sys.exit()

        return output

    def find_song(self, char, songs):
        """
            given character, this function finds
            a song where the artist name contains
            the character.
            Args:
                char - str character to find in the list of songs
            Return:
                dict - {'song': {'title': <str>, 'artist': <str>}, 'index': <int>}
        """
        for song in songs:
            index = song.get('artist').lower().find(char.lower())
            if index >= 0:
                return {'song': song, 'index': index}


def main():
    """
        main func for pop cipher
    """
    parser = ArgumentParser(description="Encrypt text using pop music")
    parser.add_argument("input_text", type=str)
    parser.add_argument("--songs-json-file", type=str, default="data.json")
    parser.add_argument("--spotify-client-id", type=str, default=None)
    parser.add_argument("--spotify-client-secret", type=str, default=None)
    parser.add_argument("--banlist", nargs='+', default=[])
    args = parser.parse_args()

    client_credentials_manager = SpotifyClientCredentials(
        args.spotify_client_id,
        args.spotify_client_secret
    )
    spotify_client = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    with open(args.songs_json_file) as songs_file:
        banlist = args.banlist
        if banlist == ["none"]:
            banlist = []

        output = PopCipher(json.load(songs_file), banlist).encrypt(args.input_text)
        for char in output:
            artist = char.get('song').get('artist')
            title = char.get('song').get('title')
            resp = spotify_client.search(q=artist + " " + title, limit=10)
            for preview_url in [x.get('preview_url') for x in resp['tracks']['items']]:
                if preview_url:
                    print(preview_url + " " + str(char.get('index') + 1))
                    break


if __name__ == '__main__':
    main()
