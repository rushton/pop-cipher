# POP CIPHER

Pop cipher is a cipher using shared cultural knowledge via music.

# Install

requires ffmpeg and lame

```
pip install -r requirements.txt
```

# Usage

## to encode a message
```
SPOTIFY_CLIENT_ID=xxx SPOTIFY_CLIENT_SECRET=xxx ./popcipher <cipher-text> <clip-length-seconds>
```

example:

```
SPOTIFY_CLIENT_ID=xxx SPOTIFY_CLIENT_SECRET=xxx ./popcipher "hi" 7
```

say the cipher chose:

Ri**h**anna - Birthday Cake

and

Rob**i**n Thicke - Blurred Lines
 

the output mp3 file will be named: `cipher_3.4.mp3`

## to decode the message

given the above example, we should have a 14 second mp3 with two 7 second clips. To do the decode:
1. listen to a clip
2. figure out who the artist is
3. take the first index (3) from the file name
4. match the index to the nth (3rd) charater of the artist's name
5. repeat for each clip

## Filtering out artists

to prevent certain artists from appearing in the cipher, pass a space-separated list to the banlist flag, -b

```
SPOTIFY_CLIENT_ID=xxx SPOTIFY_CLIENT_SECRET=xxx ./popcipher -b Nickelback ICP "hi" 7
```

## Using your own songs

to use a set of your own songs, write a file in the format:
```
[
    {
        "artist": "<artist>",
        "title": "<title>"
    },
    ...
]
```

then pass the file to pop_cipher command with the -s flag:
```
SPOTIFY_CLIENT_ID=xxx SPOTIFY_CLIENT_SECRET=xxx ./popcipher -s my_songs_file.json "hi" 7
```
