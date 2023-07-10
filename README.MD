# Discord Relay Bot (Experimental)

This project intends to create a service that can relay various
forms of information from a local program, into a Discord server, via a locally hosted Discord bot.
This project is still in its early stages of development.

## Requirements

- [Discord Bot Token](https://discord.com/developers/applications)

To run the main script, copy the token into a plain text file saved in this
directory under `config/token.txt`. The token controls access
to your Bot, so keep it safe.

## Dependencies

This bot relies heavily on the `discord.py` library, which revolves around the concept of Discord events.

_"An event is something you listen to and then respond to.
For example, when a message happens,
you will receive an event about it that you can respond to."_ -
_[discord.py/docs/basic-concepts](https://discordpy.readthedocs.io/en/latest/intro.html#basic-concepts)_

### discord.py

    pip install discord.py

### kivy

This project makes use of `kivy` to create graphical user interfaces. Kivy is a free and
open source Python framework for developing multitouch
application software. - [Read More](https://kivy.org/)

    pip install kivy

### PyNaCl

To run the `voice_joiner.py` script, which connects to a voice channel in the Discord,
you'll need to install `PyNaCl`, a library for network connection
encryption. - [Read More](https://pypi.org/project/PyNaCl/)

    pip install PyNaCl

### ffmpeg

To run the `voice_emitter.py` script, which can emit audio in a voice channel
the bot has joined, you'll need to have `ffmpeg` installed on your local machine.
FFMPEG is an open source suite of libraries for handling various types
of multimedia streaming. - [Read More](https://ffmpeg.org/)

    sudo apt install ffmpeg

### youtube-dl

To run the `voice_stream_youtube.py` script, which can stream audio from
a YouTube video into a voice channel the bot has joined, you'll need to have
`youtube-dl` installed. YouTube-DL is a free, open source command line program
to download videos from YouTube.com. - [Read More](https://github.com/ytdl-org/youtube-dl)

    pip install youtube_dl


## Contributors

- riecenaidoo
- SuperMagikarp