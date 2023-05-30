"""
Retrieves the names of all channels in the Discord
server that are visible to the bot, and displays
the information in the terminal.
"""

from typing import Any

import discord
from discord import Intents


class ChannelRetrieverClient(discord.Client):
    def __init__(self, *, intents: Intents, **options: Any):
        super().__init__(intents=intents, **options)
        self.text_channels = []
        self.voice_channels = []

    # Overrides discord.Client.on_ready - an event that can be listened for.
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        self.retrieve_channels()
        self.display_channels()

    def retrieve_channels(self):
        """Retrieves all channels in the guild that are visible
         to the bot and stores them in the class."""

        for guild in self.guilds:
            for index, channel in enumerate(guild.text_channels):
                self.text_channels.append(channel)
            for index, channel in enumerate(guild.voice_channels):
                self.voice_channels.append(channel)

    def display_channels(self):
        """Displays the directory of channels
        the bot can see in the server, separated
        by their categories."""

        print("\n[Text Channels] :")
        for index, channel in enumerate(self.text_channels):
            print(f"\t- [{index + 1}] `{channel}`")
        print("\n[Voice Channels] :")
        for index, channel in enumerate(self.voice_channels):
            print(f"\t- [{index + 1}] `{channel}`")


def run(token):
    intents = discord.Intents.default()
    intents.message_content = True

    client = ChannelRetrieverClient(intents=intents)
    client.run(token)
