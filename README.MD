# Discord Relay Bot (Experimental)

This project intends to create a service that can relay various
forms of information gathered from a client program,
into a Discord server, via a locally hosted Discord bot.

This project is still in its early stages of development.

## Requirements

- Python3 & Pip
- [Discord Bot Token](https://discord.com/developers/applications)
  - To run the script, pass the token as the environment variable `DISCORD_BOT_TOKEN`
    manually, or [using a `.env` file](https://pypi.org/project/python-dotenv/).
  - The token controls access to your Bot, so keep it safe.
- ffmpeg
  - FFMPEG is an open-source suite of libraries for handling various types
    of multimedia streaming and is required by example snippets
    streaming audio into Discord voice channels. - [Read More](https://ffmpeg.org/)
  - `sudo apt install ffmpeg` or `sudo apk add ffmpeg`


## Contributors

- riecenaidoo
- SuperMagikarp
