# POP CIPHER

Pop cipher is a cipher using shared cultural knowledge via music.

# Install

requires ffmpeg and lame:
On Mac OSX:
```
brew install ffmpeg lame
```

```
pip install -r requirements.txt
```

# Usage

## to encode a message
```
./popcipher <cipher-text> <clip-length-seconds>
```

example:

```
./popcipher "hi" 7
```

an example output might be:

```
Chosen Song: Rihanna - Birthday Cake
Chosen Song: Britney Spears - Toxic
```

where the following letters were chosen for encoding:
Chosen Song: Ri**h**anna - Birthday Cake
Chosen Song: Br**i**tney Spears - Toxic

the output mp3 file will be named: `cipher_3.3.mp3`

take a listen [here](https://raw.githubusercontent.com/rushton/pop-cipher/master/cipher_3.3.mp3)

## to decode the message

given the above example, we created a 14 second mp3 with two 7 second clips. To do the decode:
1. listen to a clip
2. figure out who the artist is
3. take the first index (3) from the file name
4. match the index to the nth (3rd) charater of the artist's name
5. repeat for each clip

## Filtering out artists

to prevent certain artists from appearing in the cipher, pass a space-separated list to the banlist flag, -b

```
./popcipher -b Nickelback ICP "hi" 7
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
./popcipher -s my_songs_file.json "hi" 7
```
