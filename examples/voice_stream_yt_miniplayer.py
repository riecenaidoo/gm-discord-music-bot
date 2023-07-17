"""Control the streamed audio of in the voice channel on the Discord."""

from typing import Any

import discord
from discord import Intents
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from youtube.YTDL import YTDLSource


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
        """Commands the bot to join a Voice Channel, emitting a sound
         when it does so.

        Will also update object state, assigning the discord.VoiceClient object,
        created during the connection process, to the `bot_in_voice_channel` field for future reference.

        :param joining_channel: The discord.VoiceChannel to have the bot connect to.
        """

        self.voice_client = await discord.VoiceChannel.connect(joining_channel)
        await self.stream_youtube_miniplayer()

    async def stream_youtube_miniplayer(self):
        """Launch a Miniplayer that can
        control the streamed audio of a YouTube video in the joined
        voice channel.
        """

        while True:  # I wish was a do-while loop
            url = input("YouTube Video > ")
            if "youtu" in url:
                break
            print("URL format appears to be incorrect.\nPlease enter a valid YouTube Video URL.")

        async with self.txt_channel.typing():
            player = await YTDLSource.from_url(url=url, loop=self.voice_client.loop, stream=True)
            self.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
            parent = self

            class Miniplayer(App):
                """"""

                def build(self):
                    grid = GridLayout(cols=2)

                    pause_button = Button(text="[Pause]")
                    resume_button = Button(text="[Resume]")

                    pause_button.bind(on_release=lambda x: parent.voice_client.pause())
                    resume_button.bind(on_release=lambda x: parent.voice_client.resume())

                    grid.add_widget(pause_button)
                    grid.add_widget(resume_button)

                    return grid

            Miniplayer().run()


def run(token):
    intents = discord.Intents.default()
    intents.message_content = True

    client = VoiceJoinerClient(intents=intents)
    client.run(token)
