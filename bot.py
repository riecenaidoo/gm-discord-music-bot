"""Discord bot functionality is handled by this module."""
import asyncio
from typing import Any

import discord
from discord import Intents 

from YTDL import YTDLSource
from console import Console, Command, StringArgsCommand, IntArgCommand
from playlist import Playlist
from async_timeout import timeout

import logging
import utils
from inspect import iscoroutinefunction


_log = logging.getLogger(__name__)
_log.addHandler(utils.HANDLER)
_log.setLevel(logging.INFO)


class MusicClient(discord.Client):
    """A Discord Client that is controllable by the host via a Console."""

    def __init__(self, *, intents: Intents, **options: Any):
        super().__init__(intents=intents, **options)
        self.voice_channels = []
        self.voice_client = None
        self.player = None
        self.playlist = Playlist()
        self.VOLUME = 0.5

    def __requires_voice_connected(func):
        log_message = f"{func.__name__}() requires the Bot to be connected a Voice Channel."
        
        if iscoroutinefunction(func):
            async def validator(self, *args, **kwargs):
                if self.voice_client is not None:
                    return await func(self, *args, **kwargs)
                else:
                    _log.warning(log_message)  
            return validator
        
        def validator(self, *args, **kwargs):
            if self.voice_client is not None:
                return func(self, *args, **kwargs)
            else:
                _log.warning(log_message)   
        return validator

    def load_voice_channels(self):
        for guild in self.guilds:
            for channel in guild.voice_channels:
                self.voice_channels.append(channel)

    async def on_ready(self):
        self.load_voice_channels()
        _log.info("MusicClient is ready for Console Commands.")

    async def quit(self):
        """Stops the MusicClient and shuts it down."""
        
        _log.info("Shutting down the MusicClient")
        if self.voice_client:
            await self.voice_leave()
        await self.close()

    # Audio Streaming Logic
    @__requires_voice_connected
    async def stream_youtube_url(self, url):
        """Plays a YouTube URL"""
        
        async with timeout(10):
            self.player = await YTDLSource.from_url(url=url, loop=self.voice_client.loop, stream=True)
            if self.player:
                _log.info(f"Now Playing {self.player.title}")
                self.player.volume = self.VOLUME
                self.voice_client.play(self.player,
                                    after=lambda e: asyncio.run_coroutine_threadsafe(self.stream_next(e),
                                                                                        self.loop))
            else:   # Skip to the next song if the AudioSource yielded nothing.
                _log.warning(f"Skipping Bad URL '{url}'.")
                await self.stream_next()

    @__requires_voice_connected
    async def stream_next(self, error=None):
        """Callback function of bot#play which is used to play through the
        songs in queue."""
        
        if error:
            _log.error(f'Player error: {error}')
        else:
            try:
                url = self.playlist.next()
                await self.stream_youtube_url(url)
            except Playlist.ExhaustedException:
                _log.info("Playlist exhausted.")

    # Voice Channel Controls
    def get_voice_channels(self):
        _log.info("Retrieving voice channels")
        for index, channel in enumerate(self.voice_channels):
            print(f"[{index}] - {channel}")

    async def voice_join(self, channel_index: int):
        if self.voice_client is not None:
            _log.debug("Bot is in a voice channel already, moving bot to new channel instead of joining.")
            await self.voice_client.move_to(self.voice_channels[channel_index])
            return

        if (channel_index >= 0) and (channel_index < len(self.voice_channels)):
            _log.debug("Joining voice channel.")
            self.voice_client = await discord.VoiceChannel.connect(self.voice_channels[channel_index])
            _log.info(f"Joined '{self.voice_channels[channel_index]}'.")
        else:
            _log.warn(f"Invalid channel index '{channel_index}'. Current voice channels available: {len(self.voice_channels)}.")

    @__requires_voice_connected
    async def voice_leave(self):
        await self.voice_client.disconnect()
        self.voice_client = None
        _log.info("Disconnected from voice channel.")
 
    # Playlist Controls
    def playlist_queue(self, urls: list[str]):
        """Add songs to the playlist."""
        
        for url in urls:
            self.playlist.add(url)
        _log.info("Added songs to queue.")

    @__requires_voice_connected
    async def playlist_start(self):
        """Starts the playlist."""
        
        _log.info("Starting playlist.")
        await self.stream_next()

    @__requires_voice_connected
    def playlist_stop(self):
        """Stops the playlist."""

        self.playlist.clear()
        self.voice_client.stop()
        _log.info("Stopped and cleared the playlist.")

    async def playlist_play(self, urls: list[str]):
        """Overrides the Playlist with new songs, playing them"""

        self.playlist.clear()
        self.playlist_queue(urls)
        await self.song_skip()      

    # Audio Controls
    @__requires_voice_connected
    def audio_pause(self):
        """Pauses the audio streaming."""
        
        self.voice_client.pause()
        _log.info("Paused the audio.")

    @__requires_voice_connected
    def audio_resume(self):
        """Resumes the audio streaming."""
        
        self.voice_client.resume()
        _log.info("Resumed the audio.")

    def set_audio_volume(self, volume: int):
        """Set the MusicClient's audio volume level."""
        
        volume = float(volume)
        volume /= 100
        if not (0.0 <= volume <= 1.0):
            _log.warn(f"Ignoring request to set `bot.volume_level` to '{int(volume*100)}' percent.")
            return
        
        if self.player is not None:
            self.player.volume = volume
            _log.debug("Adjusted active player's volume.")
               
        self.VOLUME = volume
        _log.info(f"Volume @ {int(volume*100)}%.")

    # Song Controls
    @__requires_voice_connected
    async def song_skip(self):
        """Play the next song in the playlist."""
        
        if self.voice_client.is_playing():
            _log.info("Skipped current song.")
            self.voice_client.stop()    # Triggers the callback fn 'stream_next'
        else:
            _log.info("Playing next song.")
            await self.stream_next()

    @__requires_voice_connected
    async def song_prev(self):
        """Play the previous song in the playlist."""
        
        try:
            self.playlist.add(url= self.playlist.prev(), index= 0)
            _log.info("Playing previous song.")
            await self.song_skip()
        except Playlist.ExhaustedException:
            _log.warning("No previous song. Playlist's RecentlyPlayed list is empty.")


def build_client() -> MusicClient:
    """Builds a MusicClient with necessary correct discord intents.

    Returns:
        MusicClient: MusicClient that can be started with `.start(token=token)`.
    """
    
    intents = discord.Intents.default()
    intents.message_content = True
    return MusicClient(intents=intents)


def __build_console_commands(console:Console, client:MusicClient): 
    """Builds the Commands to control a MusicClient to this Console.

    Args:
        console (Console): Console to add Commands to.
        client (MusicClient): MusicClient this Console should control. 
    """
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
    console.add_command(Command("start", client.playlist_start))
    console.add_command(Command("stop", client.playlist_stop))
    console.add_command(Command("clear", client.playlist.clear))
    console.add_command(StringArgsCommand("play", client.playlist_play))
    # Playlist Mode Controls
    console.add_command(Command("shuffle", client.playlist.shuffle_mode))
    console.add_command(Command("loop", client.playlist.loop_mode))
    console.add_command(Command("repeat", client.playlist.repeat_mode))
    console.add_command(Command("normal", client.playlist.no_looping_mode))


def build_console(client:MusicClient) -> Console:
    """Builds a Console for this MusicClient.

    Args:
        client (MusicClient): MusicClient for this Console to control.

    Returns:
        Console: Console that can control this MusicClient.
    """
    console = Console()
    __build_console_commands(console, client)
    return console