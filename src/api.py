
from flask import Flask
from flask import request
import asyncio
import functools
import typing
from bot.music_client import MusicClient

def to_thread(func: typing.Callable):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper
class APIHandler(Flask):

    def __init__(self, client:MusicClient, import_name: str):  # constructor for the APIHAndler that takes
        # a client object, so we can use it for multiple functions/clients IE. DiceRoller and the Music Player
        super().__init__(import_name)
        self.build_command_handler()
        self.client = client

    @to_thread
    def start(self, host, port):  # wrapper function for starting the API Flask server
        self.run(host=host, port=port)

    def quit():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    def build_command_handler(self):
        self.add_url_rule("/command/channel", view_func=self.get_channels)
        self.add_url_rule("/command/volume/<int:volume_number>", view_func=self.set_volume, methods=["POST"])
        self.add_url_rule("/command/join/<int:channel_number>", view_func=self.join_channel, methods=["POST"])
        self.add_url_rule("/command/leave", view_func=self.leave_channel, methods=["POST"])
        self.add_url_rule("/command/pause", view_func=self.pause, methods=["POST"])
        self.add_url_rule("/command/resume", view_func=self.resume, methods=["POST"])
        self.add_url_rule("/command/skip", view_func=self.skip)
        self.add_url_rule("/command/prev", view_func=self.previous)
        self.add_url_rule("/command/playlist/play", view_func=self.playlist_play)
        self.add_url_rule("/command/playlist/queue", view_func=self.playlist_queue)
        self.add_url_rule("/command/playlist/start", view_func=self.playlist_start)
        self.add_url_rule("/command/playlist/stop", view_func=self.playlist_stop)
        self.add_url_rule("/command/playlist/clear", view_func=self.playlist_clear)
        self.add_url_rule("/command/shuffle", view_func=self.shuffle)
        self.add_url_rule("/command/loop", view_func=self.loop_songs)
        self.add_url_rule("/command/repeat", view_func=self.repeat)
        self.add_url_rule("/command/no_loop", view_func=self.no_loop)


    def get_channels(self):
        return str(self.client.voice_channels)
    

    def leave_channel(self):
        asyncio.run_coroutine_threadsafe(self.client.voice_leave(), self.client.loop)
        return "Left Channel"

    def join_channel(self, channel_number):
        asyncio.run_coroutine_threadsafe(self.client.voice_join(channel_number), self.client.loop)
        return "Joined Channel"

    def pause(self):
        asyncio.run_coroutine_threadsafe(self.client.audio_pause(), self.client.loop)
        return "Paused"
    
    def resume(self):
        asyncio.run_coroutine_threadsafe(self.client.audio_resume(), self.client.loop)
        return "Resumed"
    
    def set_volume(self, volume_number:int):
        volume_number = request.args.get('volume_number')
        asyncio.run_coroutine_threadsafe(self.client.set_audio_volume(volume_number), self.client.loop)
        return "Volume has been set"

    def skip(self):
        asyncio.run_coroutine_threadsafe(self.client.song_skip(), self.client.loop)
        return "Skipped song"
    
    def previous(self):
        asyncio.run_coroutine_threadsafe(self.client.song_prev(), self.client.loop)
        return "Returning to Previous Song"
    
    def playlist_queue(self):
        songs = request.json['songs']
        self.client.playlist_queue(songs)
        return "Added songs to the playlist"
    
    def playlist_start(self):
        asyncio.run_coroutine_threadsafe(self.client.playlist_start(), self.client.loop)
        return "Starting Playlist..."
    
    def playlist_stop(self):
        asyncio.run_coroutine_threadsafe(self.client.playlist_stop(), self.client.loop)
        return "Playlist Stopped!"
    
    def playlist_clear(self):
        asyncio.run_coroutine_threadsafe(self.client.clear(), self.client.loop)
        return "Cleared List of Songs"
    
    def playlist_play(self):
        asyncio.run_coroutine_threadsafe(self.client.playlist_play(), self.client.loop)
        return "Playing New Playlist"
    
    def shuffle(self):
        asyncio.run_coroutine_threadsafe(self.client.shuffle_mode(), self.client.loop)
        return "Shuffled Songs"
    
    def loop_songs(self):
        asyncio.run_coroutine_threadsafe(self.client.loop_mode(), self.client.loop)
        return "Looping All Songs"
    
    def repeat(self):
        asyncio.run_coroutine_threadsafe(self.client.repeat_mode(), self.client.loop)
        return "Repeating Song..."
    
    def no_loop(self):
        asyncio.run_coroutine_threadsafe(self.client.no_looping_mode(), self.client.loop)
        return "Normal Play Resuming"
