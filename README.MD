# Discord Console Bot

A command-less Discord music bot using the Discord.py library.
The bot is controlled via the console of the host machine,
instead of slash commands in Discord.
The bot will eventually be controlled by a client program
of a socket.

## Requirements

- Python3 & Pip Package Manager
- [Discord Bot Token](https://discord.com/developers/applications)
  - To run the script, pass the token as the environment variable `DISCORD_BOT_TOKEN`
    manually, or [using a `.env` file](https://pypi.org/project/python-dotenv/).
  - The token controls access to your Bot, so keep it safe.
- ffmpeg
  - FFMPEG is an open-source suite of libraries for handling various types
    of multimedia streaming. - [Read More](https://ffmpeg.org/)
  - `sudo apt install ffmpeg` or `sudo apk add ffmpeg`


## Makefile Rules

- `make run`  : Setup the Bot's dependencies in a virtual environment and run it.
- `make help` : Bot's CLI arg help menu.
- `make dev`  : Setup dependenices for development and testing in the virtual environment.
