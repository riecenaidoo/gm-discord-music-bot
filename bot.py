"""Discord bot functionality is handled by this module."""
import asyncio
from typing import Any

import discord
from discord import Intents

from YTDL import YTDLSource
from console import Console, Command, VolumeCommand, PlayCommand, JoinChannelCommand, QueueCommand
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

    async def get_voice_channels(self):
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

        await self.clear_queue()
        await self.queue(urls)
        
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

    async def queue(self, urls: list[str]):
        for url in urls:
            self.playlist.add(url)

    async def pause(self):
        if self.voice_client is not None:
            self.voice_client.pause()

    async def resume(self):
        if self.voice_client is not None:
            self.voice_client.resume()

    async def skip_song(self):
        if self.voice_client is not None:
            self.voice_client.stop()

    async def prev_song(self):
        if self.voice_client is not None:
            try:
                self.playlist.add_first(self.playlist.prev())
                self.voice_client.stop()
            except ExhaustedException:
                print("No more songs")

    async def stop(self):
        if self.voice_client is not None:
            await self.clear_queue()
            self.voice_client.stop()

    async def start_playing(self):
        if self.voice_client is not None:
            await self.play_next()

    async def clear_queue(self):
        self.playlist.clear()

    async def set_volume(self, volume: int):
        volume = float(volume)
        volume /= 100
        if 0.0 <= volume <= 1.0:
            self.VOLUME = volume
            if self.player is not None:
                self.player.volume = self.VOLUME
        else:
            print("[WARNING] Invalid volume level!")

    async def playlist_shuffle(self):
        self.playlist.shuffle_mode()

    async def playlist_normal(self):
        self.playlist.default_mode()

    async def playlist_loop(self):
        self.playlist.loop_mode()

    async def playlist_repeat(self):
        self.playlist.repeat_mode()


class MusicClientAPI():
    
    def __init__(self, client:MusicClient, input_method:callable):
        self.CLIENT:MusicClient = client
        self.CONSOLE:Console = Console(input_method=input_method)
        self.build_console()

    def build_console(self):
        self.CONSOLE.add_command(Command("quit", self.quit))

        self.CONSOLE.add_command(Command("channels", self.get_channels))
        self.CONSOLE.add_command(JoinChannelCommand("join", self.join_channel))
        self.CONSOLE.add_command(Command("leave", self.leave_channel))

        self.CONSOLE.add_command(PlayCommand("play", self.play))

        self.CONSOLE.add_command(QueueCommand("queue", self.queue))
        self.CONSOLE.add_command(Command("clear", self.clear_queue))
        self.CONSOLE.add_command(Command("start", self.start_playing))
        self.CONSOLE.add_command(Command("stop", self.stop_playing))
        
        self.CONSOLE.add_command(Command("pause", self.pause))
        self.CONSOLE.add_command(Command("resume", self.resume))
        self.CONSOLE.add_command(VolumeCommand("volume", self.set_volume))
        
        self.CONSOLE.add_command(Command("skip", self.skip_song))
        self.CONSOLE.add_command(Command("prev", self.prev_song))
        
        self.CONSOLE.add_command(Command("shuffle", self.playlist_shuffle))
        self.CONSOLE.add_command(Command("loop", self.playlist_loop))
        self.CONSOLE.add_command(Command("repeat", self.playlist_repeat))
        self.CONSOLE.add_command(Command("normal", self.playlist_normal))
    
    async def activate(self):
        await self.CONSOLE.run()


def run(token: str, input_method: callable):
    intents = discord.Intents.default()
    intents.message_content = True

    client = MusicClient(intents=intents)
    api = MusicClientAPI(client=client,input_method=input_method)
    
    async def runner():
        client.run()
        await client.start(reconnect=True)
        await api.activate()

    try:
        asyncio.run(runner())
    except KeyboardInterrupt:
        # nothing to do here
        # `asyncio.run` handles the loop cleanup
        # and `self.start` closes all sockets and the HTTPClient instance.
        return
    