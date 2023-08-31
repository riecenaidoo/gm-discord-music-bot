"""Discord bot functionality is handled by this module."""
import asyncio
from typing import Any

import discord
from discord import Intents 

from YTDL import YTDLSource
from console import Console, Command, StringArgsCommand, IntArgCommand
from playlist import MusicQueue, ExhaustedException


class MusicClient(discord.Client):
    """A Discord Client that is controllable by the host via a Console."""

    def __init__(self, *, intents: Intents, **options: Any):
        super().__init__(intents=intents, **options)
        self.text_channels = []
        self.voice_channels = []
        self.voice_client = None
        self.player = None
        self.playlist = MusicQueue()
        self.VOLUME = 0.5

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

    async def quit(self):
        """Stops the MusicClient and shuts it down."""
        
        print("Shutting down...")
        await self.leave_channel()
        await self.close()

    # Audio Streaming Logic
    async def stream_youtube_url(self, url):
        """Plays a YouTube URL"""
        async with self.text_channels[len(self.text_channels) - 1].typing():
            self.player = await YTDLSource.from_url(url=url, loop=self.voice_client.loop, stream=True)
            self.player.volume = self.VOLUME
            self.voice_client.play(self.player,
                                   after=lambda e: asyncio.run_coroutine_threadsafe(self.stream_next(e),
                                                                                    self.loop))

    async def stream_next(self, error=None):
        """Callback function of bot#play which is used to play through the
        songs in queue."""
        if error:
            print(f'Player error: {error}')
        else:
            try:
                url = self.playlist.next()
                await self.playlist_play(url)
            except ExhaustedException:
                print("No more songs.")

    # Voice Channel Controls
    def get_voice_channels(self):
        for index, channel in enumerate(self.voice_channels):
            print(f"[{index}] - {channel}")

    async def voice_join(self, channel_index: int):
        if self.voice_client is not None:
            await self.voice_client.move_to(self.voice_channels[channel_index])
            return

        if (channel_index >= 0) and (channel_index < len(self.voice_channels)):
            self.voice_client = await discord.VoiceChannel.connect(self.voice_channels[channel_index])
        else:
            print("[WARNING] Invalid channel index!")

    async def voice_leave(self):
        if self.voice_client is not None:
            self.voice_client.stop()
            await self.voice_client.disconnect()
            self.voice_client = None

    # Playlist Controls
    def playlist_queue(self, urls: list[str]):
        """Add songs to the playlist."""
        for url in urls:
            self.playlist.add(url)

    async def playlist_start(self):
        """Starts the playlist."""
        if self.voice_client is not None:
            await self.stream_next()

    def playlist_stop(self):
        """Stops the playlist."""
        
        if self.voice_client is not None:
            self.playlist.clear()
            self.voice_client.stop()

    async def playlist_play(self, urls: list[str]):
        """Overrides the Playlist with new songs, playing them"""

        self.playlist.clear()
        self.playlist_queue(urls)
        
        if self.voice_client is None:
            return
        
        if self.voice_client.is_playing():
            self.voice_client.stop()    # Stops current AudioSource & play_next() callback triggers.
            return
        
        await self.stream_next()


    # Audio Controls
    def audio_pause(self):
        """Pauses the audio streaming."""
        
        if self.voice_client is not None:
            self.voice_client.pause()

    def audio_resume(self):
        """Resumes the audio streaming."""
        
        if self.voice_client is not None:
            self.voice_client.resume()

    def set_audio_volume(self, volume: int):
        """Set the MusicClient's audio volume level."""
        
        volume = float(volume)
        volume /= 100
        if not (0.0 <= volume <= 1.0):
            print("[WARNING] Invalid volume level!")
            return
        
        if self.player is not None:
            self.player.volume = volume    
        self.VOLUME = volume

    # Song Controls
    def song_skip(self):
        """Play the next song in the playlist."""
        
        if self.voice_client is not None:
            self.voice_client.stop()

    def song_prev(self):
        """Play the previous song in the playlist."""
        
        if self.voice_client is not None:
            try:
                self.playlist.add_first(self.playlist.prev())
                self.voice_client.stop()
            except ExhaustedException:
                print("No more songs")


def build_console(console:Console, client:MusicClient):    
    # Primary Controls
    console.add_command(StringArgsCommand("play", client.playlist_play))
    console.add_command(Command("quit", client.quit))
    # Voice Channel Controls
    console.add_command(Command("channels", client.get_voice_channels))
    console.add_command(IntArgCommand("join", client.voice_join))
    console.add_command(Command("leave", client.voice_leave))
    # Audio Controls
    console.add_command(Command("pause", client.audio_pause))
    console.add_command(Command("resume", client.audio_resume))
    console.add_command(IntArgCommand("volume", client.set_audio_volume))
    # Song Controls
    console.add_command(Command("skip", client.song_skip))
    console.add_command(Command("prev", client.song_prev))
    # Playlist Controls
    console.add_command(StringArgsCommand("queue", client.playlist_queue))
    console.add_command(Command("clear", client.playlist.clear))
    console.add_command(Command("start", client.playlist_start))
    console.add_command(Command("stop", client.playlist_stop))
    # Playlist Mode Controls
    console.add_command(Command("shuffle", client.playlist.shuffle_mode))
    console.add_command(Command("loop", client.playlist.loop_mode))
    console.add_command(Command("repeat", client.playlist.repeat_mode))
    console.add_command(Command("normal", client.playlist.default_mode))

def get_client() -> MusicClient:
    intents = discord.Intents.default()
    intents.message_content = True
    return MusicClient(intents=intents)

def get_console(client:MusicClient) -> Console:
    console = Console()
    build_console(console, client)
    return console