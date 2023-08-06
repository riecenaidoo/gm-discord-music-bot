"""Stream the audio from multiple YouTube videos,
one by one, into a voice channel in the Discord."""
import asyncio
from typing import Any

import discord
from discord import Intents

from YTDL import YTDLSource


class VoiceJoinerClient(discord.Client):
    def __init__(self, *, intents: Intents, **options: Any):
        super().__init__(intents=intents, **options)
        self.voice_channels = []
        self.joined_channel = None
        self.voice_client = None
        self.txt_channel = None

    # Overrides discord.Client.on_ready - an event that can be listened for.
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        self.retrieve_voice_channels()

        for guild in self.guilds:
            for index, channel in enumerate(guild.text_channels):
                self.txt_channel = channel
                break

        await self.join_voice_channel(self.select_joining_channel())

    # Helper Methods
    def retrieve_voice_channels(self):
        """Retrieves all Voice channels in the guild that are visible
        to the bot and stores them in the class.

        :return:
        """

        for guild in self.guilds:
            for index, channel in enumerate(guild.voice_channels):
                self.voice_channels.append(channel)

    def display_channels(self):
        """Displays the directory of Voice channels the bot can see in the server."""

        print("\n[Voice Channels] :")
        for index, channel in enumerate(self.voice_channels):
            print(f"\t- [{index + 1}] `{channel}`")

    def select_joining_channel(self):
        """ Selects a Voice Channel in the Server to join.

        :return: discord.VoiceChannel - The Voice Channel the user selects.
        """

        self.display_channels()

        choice_index = None
        while choice_index is None:
            choice_index = input("Join Channel No. > ")
            try:
                choice_index = (int(choice_index) - 1)
            except ValueError:
                print("Please select a No.")
                choice_index = None

            if choice_index < 0 or choice_index > (len(self.voice_channels) - 1):
                print("Please select a Voice Channel No.")
                choice_index = None

        return self.voice_channels[choice_index]

    async def join_voice_channel(self, joining_channel):
        """Commands the bot to join a Voice Channel, playing audio from
         a YouTube video when it does so, and continuing the process repeatedly.

        Will also update object state, assigning the discord.VoiceClient object,
        created during the connection process, to the `bot_in_voice_channel` field for future reference.

        :param joining_channel: The discord.VoiceChannel to have the bot connect to.
        """

        self.voice_client = await discord.VoiceChannel.connect(joining_channel)
        await self.stream_youtube(get_url())

    async def stream_youtube(self, url: str):
        """Stream the audio of a YouTube video in the joined channel."""

        async with self.txt_channel.typing():
            player = await YTDLSource.from_url(url=url, loop=self.voice_client.loop, stream=True)
            self.voice_client.play(player,
                                   after=lambda e: asyncio.run_coroutine_threadsafe(self.after_play(e), self.loop))

    async def after_play(self, error):
        if error:
            print(f'Player error: {error}')
        else:
            await self.stream_youtube(get_url())


def get_url() -> str:
    """
    :return: str containing a URL.
    """

    while True:  # I wish was a do-while loop
        url = input("YouTube Video > ")
        if "youtu" in url:
            return url
        print("URL format appears to be incorrect.\nPlease enter a valid YouTube Video URL.")


def run(token):
    intents = discord.Intents.default()
    intents.message_content = True

    client = VoiceJoinerClient(intents=intents)
    client.run(token)
