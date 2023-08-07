"""Discord bot functionality is handled by this module."""
import discord
from discord import Intents
from typing import Any
from YTDL import YTDLSource
from console import Console, Command, VolumeCommand, PlayCommand, JoinChannelCommand

class ConsoleClient(discord.Client):
    """A Discord Client that is controllable by the host via a Console."""

    def __init__(self, *, input_method: callable, intents: Intents, **options: Any):
        super().__init__(intents=intents, **options)
        self.console = Console(input_method=input_method)
        self.build_console()
        self.text_channels = []
        self.voice_channels = []
        self.voice_client = None
        self.player = None

    def build_console(self):
        self.console.add_command(PlayCommand("play", self.play_url))
        self.console.add_command(Command("pause", self.pause))
        self.console.add_command(Command("resume", self.resume))
        self.console.add_command(VolumeCommand("volume", self.set_volume))
        self.console.add_command(Command("channels", self.get_voice_channels))
        self.console.add_command(JoinChannelCommand("join", self.join_channel))
        self.console.add_command(Command("leave", self.leave_channel))
        self.console.add_command(Command("quit", self.quit))

    def load_voice_channels(self):
        for guild in self.guilds:
            for channel in guild.voice_channels:
                self.voice_channels.append(channel)

    def load_text_channels(self):
        for guild in self.guilds:
            for channel in guild.text_channels:
                self.text_channels.append(channel)

    async def on_ready(self):
        self.load_voice_channels()
        self.load_text_channels()
        await self.console.run()

    async def quit(self):
        print("[INFO] Shutting down...")
        self.console.online = False
        # TODO: Close quietly by stopping the music player
        await self.leave_channel()
        await self.close()

    async def get_voice_channels(self):
        for index, channel in enumerate(self.voice_channels):
            print(f"[{index}] - {channel}")

    async def join_channel(self, channel_index: int):
        if self.voice_client is not None:
            # TODO: Joining while already in a channel should trigger a move_to
            print("[WARNING] Already in a channel!")
            return

        if (channel_index >= 0) and (channel_index < len(self.voice_channels)):
            self.voice_client = await discord.VoiceChannel.connect(self.voice_channels[channel_index])
        else:
            print("[WARNING] Invalid channel index!")

    async def leave_channel(self):
        # TODO: Should stop player before leaving a channel
        if self.voice_client is not None:
            await self.voice_client.disconnect()
            self.voice_client = None

    async def play_url(self, url: str):
        if self.voice_client is not None:
            async with self.text_channels[len(self.text_channels)-1].typing():
                self.player = await YTDLSource.from_url(url=url, loop=self.voice_client.loop, stream=True)
                self.voice_client.play(self.player, after=lambda e: print(f'Player error: {e}') if e else None)

    async def pause(self):
        if self.player is not None:
            self.voice_client.pause()

    async def resume(self):
        if self.player is not None:
            self.voice_client.resume()

    async def set_volume(self, volume: int):
        if self.player is not None:
            volume = float(volume)
            volume /= 100
            if 0.0 < volume <= 1.0:
                self.player.volume = volume
            else:
                print("[WARNING] Invalid volume level!")


def run(token: str, input_method: callable):
    intents = discord.Intents.default()
    intents.message_content = True

    client = ConsoleClient(intents=intents, input_method=input_method)
    client.run(token)
