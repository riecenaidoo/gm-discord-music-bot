import asyncio
import functools
import os
import typing
from typing import Any

import discord
from discord import Intents
from dotenv import load_dotenv

import console
from console import Console, Command, VolumeCommand, PlayCommand


def to_thread(func: typing.Callable):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper


class ConsoleClient(discord.Client):
    def __init__(self, *, input_method: callable, intents: Intents, **options: Any):
        super().__init__(intents=intents, **options)
        self.console = Console(input_method=input_method)

        self.console.add_command(PlayCommand("play", self.play_url))
        self.console.add_command(VolumeCommand("volume", self.set_volume))
        self.console.add_command(Command("quit", self.quit))

    async def on_ready(self):
        await self.console.run()

    async def quit(self):
        print(f"[QUIT]")
        self.console.online = False
        await self.close()

    async def show_channels(self):
        pass

    async def join_channel(self, channel_index: int):
        pass

    async def play_url(self, url: str):
        pass

    async def pause(self):
        pass

    async def resume(self):
        pass

    async def set_volume(self, volume: int):
        pass


def run(token):
    intents = discord.Intents.default()
    intents.message_content = True

    client = ConsoleClient(intents=intents, input_method=console.get_user_input)
    client.run(token)


if __name__ == '__main__':
    load_dotenv()
    run(token=os.environ["DISCORD_BOT_TOKEN"])
