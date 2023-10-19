import discord
from flask import Flask
from flask import request
import json
import asyncio
import functools
import typing

def to_thread(func: typing.Callable):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper
class APIHandler(Flask):

    def __init__(self, client, import_name: str):  # constructor for the APIHAndler that takes
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
        self.add_url_rule("/command/join/<int:channel_number>", view_func=lambda channel_number: self.join_channel(channel_number), methods=["POST"])
        self.add_url_rule("/command/leave", view_func=self.leave_channel)
        self.add_url_rule("/command/pause", view_func=self.pause)

    def get_channels(self):
        return str(self.client.voice_channels)
    

    def leave_channel(self):
        asyncio.run_coroutine_threadsafe(self.client.voice_leave, self.client.loop)
        return "Left Channel"

    def join_channel(self, channel_id):
        asyncio.run_coroutine_threadsafe(self.client.voice_leave(channel_id), self.client.loop)
        return "Joined Channel"

    def pause(self):
        asyncio.run_coroutine_threadsafe(self.client.audio_pause, self.client.loop)
        return "Paused"
    
    def resume(self):
        asyncio.run_coroutine_threadsafe(self.client.audio_resume, self.client.loop)
        return "Resumed"
    
    def volume(self):
        asyncio.run_coroutine_threadsafe(self.client.set_audio_volume, self.client.loop)
        return "Volume has been set"

    def skip(self):
        asyncio.run_coroutine_threadsafe(self.client.song_skip, self.client.loop)
        return "Skipped song"
    
    def previous(self):
        asyncio.run_coroutine_threadsafe(self.client.song_prev, self.client.loop)
        return "Returning to Previous Song"
    
    def 

def run():
    intents = discord.Intents.default()
    intents.message_content = True
