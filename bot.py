import asyncio
import functools
import os
import typing
from typing import Any

import discord
from discord import Intents
from dotenv import load_dotenv

from console import Console, VolumeCommand, PlayCommand, get_console_input


def to_thread(func: typing.Callable):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper


class ConsoleClient(discord.Client):
    def __init__(self, *, intents: Intents, **options: Any):
        super().__init__(intents=intents, **options)

    async def on_ready(self):
        console = Console(input_method=get_console_input)

        console.add_command(PlayCommand("play", self.play_url))
        console.add_command(VolumeCommand("volume", self.set_volume))

        await to_thread(console.run)()

    async def play_url(self, url: str):
        print(f"[PLAY] {url}")

    async def set_volume(self, volume: int):
        print(f"[VOLUME] {volume}")


def run(token):
    intents = discord.Intents.default()
    intents.message_content = True

    client = ConsoleClient(intents=intents)
    client.run(token)


if __name__ == '__main__':
    load_dotenv()
    run(token=os.environ["DISCORD_BOT_TOKEN"])
