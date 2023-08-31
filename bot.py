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
        print("[INFO] Shutting down...")
        self.console.online = False
        await self.leave_channel()
        await self.close()

    def get_voice_channels(self):
        for index, channel in enumerate(self.voice_channels):
            print(f"[{index}] - {channel}")

    async def join_channel(self, channel_index: int):
        if self.voice_client is not None:
            await self.voice_client.move_to(self.voice_channels[channel_index])
            return

        if (channel_index >= 0) and (channel_index < len(self.voice_channels)):
            self.voice_client = await discord.VoiceChannel.connect(self.voice_channels[channel_index])
        else:
            print("[WARNING] Invalid channel index!")

    async def leave_channel(self):
        if self.voice_client is not None:
            self.voice_client.stop()
            await self.voice_client.disconnect()
            self.voice_client = None

    async def play_now(self, urls: list[str]):
        """Overrides the queue with a new selection of songs, playing them immediately."""

        self.clear_queue()
        self.queue(urls)
        
        if self.voice_client is None:
            return
        
        if self.voice_client.is_playing():
            self.voice_client.stop()    # Stops current AudioSource & play_next() callback triggers.
            return
        
        await self.start_playing()

    async def play(self, url):
        """Plays a YouTube URL"""
        async with self.text_channels[len(self.text_channels) - 1].typing():
            self.player = await YTDLSource.from_url(url=url, loop=self.voice_client.loop, stream=True)
            self.player.volume = self.VOLUME
            self.voice_client.play(self.player,
                                   after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(e),
                                                                                    self.loop))

    async def play_next(self, error=None):
        """Callback function of bot#play which is used to play through the
        songs in queue."""
        if error:
            print(f'Player error: {error}')
        else:
            try:
                url = self.playlist.next()
                await self.play(url)
            except ExhaustedException:
                print("No more songs.")

    def queue(self, urls: list[str]):
        for url in urls:
            self.playlist.add(url)

    def pause(self):
        if self.voice_client is not None:
            self.voice_client.pause()

    def resume(self):
        if self.voice_client is not None:
            self.voice_client.resume()

    def skip_song(self):
        if self.voice_client is not None:
            self.voice_client.stop()

    def prev_song(self):
        if self.voice_client is not None:
            try:
                self.playlist.add_first(self.playlist.prev())
                self.voice_client.stop()
            except ExhaustedException:
                print("No more songs")

    def stop(self):
        if self.voice_client is not None:
            self.clear_queue()
            self.voice_client.stop()

    async def start_playing(self):
        if self.voice_client is not None:
            await self.play_next()

    def clear_queue(self):
        self.playlist.clear()

    def set_volume(self, volume: int):
        volume = float(volume)
        volume /= 100
        if 0.0 <= volume <= 1.0:
            self.VOLUME = volume
            if self.player is not None:
                self.player.volume = self.VOLUME
        else:
            print("[WARNING] Invalid volume level!")


class MusicClientAPI():
    
    def __init__(self, client:MusicClient, input_method:callable):
        self.CLIENT:MusicClient = client
        self.CONSOLE:Console = Console(input_method=input_method)
        self.build_console()

    async def activate(self):
        await self.CONSOLE.run()

    def build_console(self):
        # Primary Controls
        self.CONSOLE.add_command(StringArgsCommand("play", self.play))
        self.CONSOLE.add_command(Command("quit", self.quit))
        # Voice Channel Controls
        self.CONSOLE.add_command(Command("channels", self.get_voice_channels))
        self.CONSOLE.add_command(IntArgCommand("join", self.voice_join))
        self.CONSOLE.add_command(Command("leave", self.voice_leave))
        # Audio Controls
        self.CONSOLE.add_command(Command("pause", self.audio_pause))
        self.CONSOLE.add_command(Command("resume", self.audio_resume))
        self.CONSOLE.add_command(IntArgCommand("volume", self.audio_volume))
        # Song Controls
        self.CONSOLE.add_command(Command("skip", self.song_skip))
        self.CONSOLE.add_command(Command("prev", self.song_prev))
        # Playlist Controls
        self.CONSOLE.add_command(StringArgsCommand("queue", self.playlist_queue))
        self.CONSOLE.add_command(Command("clear", self.playlist_clear))
        self.CONSOLE.add_command(Command("start", self.playlist_start))
        self.CONSOLE.add_command(Command("stop", self.playlist_stop))
        # Playlist Mode Controls
        self.CONSOLE.add_command(Command("shuffle", self.playlist_mode_shuffle))
        self.CONSOLE.add_command(Command("loop", self.playlist_mode_loop))
        self.CONSOLE.add_command(Command("repeat", self.playlist_mode_repeat))
        self.CONSOLE.add_command(Command("normal", self.playlist_mode_normal))

    # Primary Controls
    async def play(self):
        pass
    
    async def quit(self):
        pass
    # Voice Channel Controls
    async def get_voice_channels(self):
        pass
    
    async def voice_join(self):
        pass
    
    async def voice_leave(self):
        pass
    # Audio Controls
    async def audio_pause(self):
        pass
    
    async def audio_resume(self):
        pass
    
    async def audio_volume(self):
        pass
    # Song Controls
    async def song_skip(self):
        pass
    
    async def song_prev(self):
        pass
    # Playlist Controls
    async def playlist_queue(self):
        pass
    async def playlist_clear(self):
        pass
    async def playlist_start(self):
        pass
    async def playlist_stop(self):
        pass
    # Playlist Mode Controls
    async def playlist_mode_shuffle(self):
        self.CLIENT.playlist.shuffle_mode()
        
    async def playlist_mode_loop(self):
        self.CLIENT.playlist.loop_mode()
        
    async def playlist_mode_repeat(self):
        self.CLIENT.playlist.repeat_mode()
        
    async def playlist_mode_normal(self):
        self.CLIENT.playlist.default_mode()


def run(token: str, input_method: callable):
    intents = discord.Intents.default()
    intents.message_content = True

    client = MusicClient(intents=intents)
    api = MusicClientAPI(client=client,input_method=input_method)
    
    async def runner():
        discord.utils.setup_logging()
        await client.start(token=token, reconnect=True)
        await api.activate()

    try:
        asyncio.run(runner())
    except KeyboardInterrupt:
        # nothing to do here
        # `asyncio.run` handles the loop cleanup
        # and `self.start` closes all sockets and the HTTPClient instance.
        return
    