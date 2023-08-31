"""Asynchronous console controls for the Discord bot are managed by this module."""
import asyncio
import functools
import typing
from inspect import iscoroutinefunction

def to_thread(func: typing.Callable):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper


class Command:

    def __init__(self, name_match: str, action_func: callable):
        self.name_match = name_match.strip().casefold()
        self.action_func = action_func

    def match(self, arg: str) -> bool:
        return arg.strip().casefold() == self.name_match

    async def call(self, args: list[str]):
        if(iscoroutinefunction(self.action_func)):
            await self.action_func()
        else:
            self.action_func()


class PlayCommand(Command):

    async def call(self, args: list[str]):
        if len(args) < 2:
            raise UsageError(f"{self.name_match} expects an argument")

        await self.action_func(args[1:])


class VolumeCommand(Command):

    async def call(self, args: list[str]):
        if len(args) < 2:
            raise UsageError(f"{self.name_match} expects an argument")

        volume = args[1]

        try:
            volume = int(volume)
        except ValueError:
            raise UsageError(f"{self.name_match} argument must be integer")

        if volume < 0 or volume > 100:
            raise UsageError(f"{self.name_match} must be between 0 & 100")

        await self.action_func(volume)


class JoinChannelCommand(Command):

    async def call(self, args: list[str]):
        if len(args) < 2:
            raise UsageError(f"{self.name_match} expects an argument")

        index = args[1]

        try:
            index = int(index)
        except ValueError:
            raise UsageError(f"{self.name_match} argument must be integer")

        if index < 0:
            raise UsageError(f"{self.name_match} must be index (greater than 0)")

        await self.action_func(index)


class QueueCommand(Command):

    async def call(self, args: list[str]):
        if len(args) < 2:
            raise UsageError(f"{self.name_match} expects an argument")

        await self.action_func(args[1:])


class Console:

    def __init__(self, input_method: callable):
        self.commands = list()
        self.input_method = to_thread(input_method)
        self.online = True

    def add_command(self, command: Command):
        self.commands.append(command)

    async def handle_command(self, args: list[str]):
        for cmd in self.commands:
            if cmd.match(args[0]):
                await cmd.call(args)
                break
        else:
            print("No match")

    async def run(self):
        while self.online:
            try:
                user_in = await self.input_method()
                await self.handle_command(user_in)
            except UsageError as e:
                print(f"Usage Error: {e.args[0]}")


class UsageError(Exception):
    pass
