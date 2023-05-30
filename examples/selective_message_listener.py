"""
Allows the Client to select a specific Text
channel in the Discord server, and display messages
from that channel only in the terminal.
"""

from typing import Any

import discord
from discord import Intents


class SelectiveMessageListenerClient(discord.Client):
    def __init__(self, *, intents: Intents, **options: Any):
        super().__init__(intents=intents, **options)
        self.text_channels = []
        self.listening_channel = None

    # Overrides discord.Client.on_ready - an event that can be listened for.
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        self.retrieve_text_channels()
        self.select_listening_channel()

    # Overrides discord.Client.on_message - an event that can be listened for.
    async def on_message(self, message):
        """Triggers during on_message events in the Server,
        this function will display Text Channel messages from the
        Server in the Client terminal, filtering the messages
        to only display messages received from a selected channel."""

        if message.channel is self.listening_channel:
            print(f'Message from {message.author}: {message.content}')

    # Helper Methods
    def retrieve_text_channels(self):
        """Retrieves all text channels in the guild that are visible
         to the bot and stores them in the class."""

        for guild in self.guilds:
            for index, channel in enumerate(guild.text_channels):
                self.text_channels.append(channel)

    def display_channels(self):
        """Displays the directory of text channels
        the bot can see in the server."""

        print("\n[Text Channels] :")
        for index, channel in enumerate(self.text_channels):
            print(f"\t- [{index + 1}] `{channel}`")

    def select_listening_channel(self):
        """ Selects a Text Channel in the Server to
        listen to, displaying that Channel's messages in the terminal.
        """

        self.display_channels()

        choice_index = None
        while choice_index is None:
            choice_index = input("Listen to Channel No. > ")
            try:
                choice_index = (int(choice_index) - 1)
            except ValueError:
                print("Please select a No.")
                choice_index = None

            if choice_index < 0 or choice_index > (len(self.text_channels) - 1):
                print("Please select a Text Channel No.")
                choice_index = None

        self.listening_channel = self.text_channels[choice_index]


def run(token):
    intents = discord.Intents.default()
    intents.message_content = True

    client = SelectiveMessageListenerClient(intents=intents)
    client.run(token)
