from argparse import ArgumentParser
import json
from random import shuffle
import requests

import sys
from sys import stderr

MAX_SONG_SEARCH_ATTEMPTS = 5


class PopCipher(object):
    """
        class for encrypting text using pop cipher
    """
    def __init__(self, songs):
        """
            Args:
                songs - list[dict] of [{'title': <str>, 'artist': <str>}, ...]
        """
        self.songs = songs

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

            shuffle(self.songs)
            shuffle(low_pri_songs)
            high_pri_songs = [s for s in self.songs if s not in low_pri_songs]
            song = self.find_song(char, high_pri_songs) or self.find_song(char, low_pri_songs)

            if song:
                output.append(song)
                if song not in low_pri_songs:
                    low_pri_songs.append(song.get('song'))

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
            indexes = [i for (i, c) in enumerate(song.get('artist').lower()) if c == char.lower()]
            shuffle(indexes)
            if len(indexes) > 0:
                return {'song': song, 'index': indexes[0]}


def is_valid(songs, input_text):
    """
        Args:
            songs - list[dict] of [{'title': <str>, 'artist': <str>}, ...]
            input_text - str text to be encoded
        Return:
            bool - True if the text can be encoded given the list of songs
    """
    return set(input_text.lower()).issubset(set(''.join([x.get('artist') for x in songs]).lower()))


def find_preview_url(artist, title):
    """

    """
    search_term = {'term': artist + " " + title}
    resp = requests.get("https://itunes.apple.com/search", params=search_term)

    for preview_url in [x.get('previewUrl') for x in resp.json().get('results')]:
        if preview_url:
            return preview_url
            break
    raise Exception("Couldn't find preview url for: %s - %s" % (artist, title))


def main():
    """
        main func for pop cipher
    """
    parser = ArgumentParser(description="Encrypt text using pop music")
    parser.add_argument("input_text", type=str)
    parser.add_argument("--songs-json-file", type=str, default="data.json")
    parser.add_argument("--banlist", nargs='+', default=[])
    args = parser.parse_args()

    with open(args.songs_json_file) as songs_file:
        banlist = [artist.lower() for artist in args.banlist]
        if banlist == ["none"]:
            banlist = []

        songs = [song for song in json.load(songs_file) if song.get('artist').lower() not in banlist]
        if not is_valid(songs, args.input_text):
            stderr.write("Unable to encode text '%s' with songs list in: %s\n" % (args.input_text, args.songs_json_file))
            sys.exit(1)

        output = PopCipher(songs).encrypt(args.input_text)
        for char in output:
            artist = char.get('song').get('artist')
            title = char.get('song').get('title')
            stderr.write("Chosen Song: %s - %s\n" % (artist, title))
            print(find_preview_url(artist, title) + " " + str(char.get('index') + 1))


if __name__ == '__main__':
    main()
