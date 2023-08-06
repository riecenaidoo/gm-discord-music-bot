import asyncio
import functools
import os
import typing
from typing import Any

import discord
from discord import Intents
from dotenv import load_dotenv

from YTDL import YTDLSource


def to_thread(func: typing.Callable):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper


class VoiceJoinerClient(discord.Client):
    def __init__(self, *, intents: Intents, **options: Any):
        super().__init__(intents=intents, **options)
        self.voice_channels = []
        self.joined_channel = None
        self.voice_client = None
        self.txt_channel = None
        self.songs = []

        self.songs.append("https://youtu.be/DW0Xp4GKtZU")
        self.songs.append("https://youtu.be/aoTmaVrQi60")
        self.songs.append("https://youtu.be/NKGm4wDfUZE")
        self.songs.append("https://youtu.be/brEROnzYULo")

    # Overrides discord.Client.on_ready - an event that can be listened for.
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        for guild in self.guilds:
            for index, channel in enumerate(guild.text_channels):
                self.txt_channel = channel
                break

        for guild in self.guilds:
            for index, channel in enumerate(guild.voice_channels):
                self.voice_channels.append(channel)

        if len(self.voice_channels) > 0:
            await self.join_voice_channel(self.voice_channels[0])
        else:
            print("[BAD] There were no voice channels for the bot to join.")

    async def join_voice_channel(self, joining_channel):
        """Commands the bot to join a Voice Channel, playing audio from
         a YouTube video when it does so, and continuing the process repeatedly.

        Will also update object state, assigning the discord.VoiceClient object,
        created during the connection process, to the `bot_in_voice_channel` field for future reference.

        :param joining_channel: The discord.VoiceChannel to have the bot connect to.
        """

        self.voice_client = await discord.VoiceChannel.connect(joining_channel)
        await self.stream_youtube(self.songs.pop())

        miniplayer_on = await self.call_miniplayer()
        while miniplayer_on:
            miniplayer_on = await self.call_miniplayer()

    @to_thread
    def call_miniplayer(self):
        cmd = input("[PAUSE/PLAY/QUIT] > ").casefold()
        if cmd == "QUIT".casefold():
            return False
        elif cmd == "PAUSE".casefold():
            self.voice_client.pause()
        elif cmd == "PLAY".casefold():
            self.voice_client.resume()
        return True

    async def stream_youtube(self, url: str):
        """Stream the audio of a YouTube video in the joined channel."""

        async with self.txt_channel.typing():
            player = await YTDLSource.from_url(url=url, loop=self.voice_client.loop, stream=True)
            self.voice_client.play(player,
                                   after=lambda e: asyncio.run_coroutine_threadsafe(self.after_play(e), self.loop))

    async def after_play(self, error):
        if error:
            print(f'Player error: {error}')
        elif len(self.songs) <= 0:
            print("Song queue empty.")
        else:
            await self.stream_youtube(self.songs.pop())


def run(token):
    intents = discord.Intents.default()
    intents.message_content = True

    client = VoiceJoinerClient(intents=intents)
    client.run(token)


if __name__ == '__main__':
    load_dotenv()
    run(token=os.environ["DISCORD_BOT_TOKEN"])
