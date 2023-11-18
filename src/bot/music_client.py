"""Contains `MusicClient`, an extension of `discord.Client` that manages
the streaming of music playlists in a Discord server."""

import logging
import time
import typing
from inspect import iscoroutinefunction

import asyncio
import discord
from async_timeout import timeout
from discord import Intents

import utils
from .yt_source import YTDLSource
from .playlist import Playlist


_log = logging.getLogger(__name__)
_log.addHandler(utils.HANDLER)
_log.setLevel(logging.INFO)


class MusicClient(discord.Client):
    """Discord Client that manages the streaming of music into voice channels."""

    def __init__(self, *, intents: Intents, **options: typing.Any):
        super().__init__(intents=intents, **options)
        self.voice_channels = []
        self.voice_client = None
        self.player = None
        self.playlist = Playlist()
        self.volume = 0.5

    @staticmethod
    def __requires_voice_connected(func: typing.Callable):
        """Validate the Bot is in a voice channel before invoking the wrapped method."""
        log_message = "%s() requires the Bot to be connected a Voice Channel."
        if iscoroutinefunction(func):
            async def validator(self, *args, **kwargs):
                if self.voice_client is not None:
                    return await func(self, *args, **kwargs)
                _log.warning(log_message, func.__name__)
            return validator
        def validator(self, *args, **kwargs):
            if self.voice_client is not None:
                return func(self, *args, **kwargs)
            _log.warning(log_message, func.__name__)
        return validator

    def load_voice_channels(self):
        """Initialise the list of voice channels in server.
        Used to know which channels are available for the MusicClient
        to join.
        """
        for guild in self.guilds:
            for channel in guild.voice_channels:
                self.voice_channels.append(channel)

    async def on_ready(self):
        """|event| Client has connectet to Discord."""
        self.load_voice_channels()
        _log.info("MusicClient is ready for Console Commands.")

    async def quit(self):
        """Stops the MusicClient and shuts it down."""
        _log.debug("Shutting down the MusicClient.")
        if self.voice_client:
            await self.voice_leave()
            _log.debug("Leaving time for player's callback to resolve.")
            time.sleep(2)
        await self.close()
        _log.info("Bot has shutdown.")

    # Audio Streaming Logic
    @__requires_voice_connected
    async def _stream_youtube_url(self, url:str):
        """|coro| Streams a song from YouTube in the connected voice channel.

        Will attempt to validate the Bot's state before playing the requested song,
        to avoid crashing the Bot service, this may result in songs being skipped/
        play requests being ignored.

        Callbacks to `stream_next` to cycle through the playlist.

        Args:
            url (str): YouTube URL of the song to stream.
        """
        async with timeout(10):
            self.player = await YTDLSource.from_url(url=url, loop=self.voice_client.loop,
                                                    stream=True)
            if self.player:
                if self.voice_client.is_playing():
                    _log.error("Audio Player requested to play audio, "
                               + "while already playing audio.\nLikely a usage error, "
                               + "or async event-loop failure. Was the Bot shutting down?")
                    return
                _log.info("Now Playing: \"%s\".", self.player.title)
                self.player.volume = self.volume
                self.voice_client.play(self.player,
                                    after=lambda e: asyncio.run_coroutine_threadsafe(
                                        self.stream_next(e), self.loop))
            else:   # Skip to the next song if the AudioSource yielded nothing.
                _log.warning("Skipping Bad URL '%s'.", url)
                await self.stream_next()

    @__requires_voice_connected
    async def stream_next(self, error=None):
        """Callback function of bot#play which is used to play through the
        songs in queue."""
        if error:
            _log.error('Player error: %s', error)
        else:
            try:
                url = self.playlist.next()
                await self._stream_youtube_url(url)
            except Playlist.ExhaustedException:
                _log.info("Playlist exhausted.")

    # Voice Channel Controls
    def get_voice_channels(self):
        """Display voice channels of server by index."""
        _log.info("Retrieving voice channels")
        for index, channel in enumerate(self.voice_channels):
            print(f"[{index}] - {channel}")

    async def voice_join(self, channel_index: int):
        """Join voice channel by index in server."""
        if self.voice_client is not None:
            _log.debug("Bot is in a voice channel already,"
                       + " moving bot to new channel instead of joining.")
            await self.voice_client.move_to(self.voice_channels[channel_index])
            return
        if  0 <= channel_index < len(self.voice_channels):
            _log.debug("Joining voice channel.")
            self.voice_client = await discord.VoiceChannel.connect(
                self.voice_channels[channel_index])
            _log.info("Joined '%s'.", self.voice_channels[channel_index])
        else:
            _log.warning("Invalid channel index '%s'. Current voice channels available: %s.",
                      channel_index, len(self.voice_channels))

    @__requires_voice_connected
    async def voice_leave(self):
        """Leave current voice channel."""
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
        if not 0.0 <= volume <= 1.0:
            _log.warning("Ignoring request to set `bot.volume_level` to '%s' percent.",
                      int(volume*100))
            return
        if self.player is not None:
            self.player.volume = volume
            _log.debug("Adjusted active player's volume.")
        self.volume = volume
        _log.info("Volume @ %s%.", int(volume*100))

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
