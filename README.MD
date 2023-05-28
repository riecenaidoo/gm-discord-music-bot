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
