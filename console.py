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
    """Wraps a callable function under an alias. 
    
    Can be extended from to validate and pass arguments to the callable function.
    """

    def __init__(self, alias: str, command_func: callable):
        """Wraps a callable function under an alias.

        Args:
            alias (str): the string that will trigger a match for this Command.
            command_func (callable): the function to be called when this Command is matched.
        """
        self.alias = alias.strip().casefold()
        self.command_func = command_func

    def match(self, arg: str) -> bool:
        """Checks whether this Command has been matched.

        Args:
            arg (str): The string to check against this Command's alias.

        Returns:
            bool: True if the arg matches this Command.
        """
        return arg.strip().casefold() == self.alias

    async def call(self, args: list[str]):
        """Calls this Command's function. If the function is a coroutine, it will await it.

        Args:
            args (list[str]): Placeholder for arguments to be passed to a callable func. Used when call is overriden by inheritors.
        """
        if(iscoroutinefunction(self.command_func)):
            await self.command_func()
        else:
            self.command_func()

    class UsageError(Exception):
        """Raised by an extended Command if the additional arguments received
        for the Command were invalid.
        """
        pass

class StringArgsCommand(Command):
    """Overriden Command that passes many string args to its callable function."""
    async def call(self, args: list[str]):
        if len(args) < 2:
            raise self.UsageError(f"{self.alias} expects an argument")

        if(iscoroutinefunction(self.command_func)):
            await self.command_func(args[1:])
        else:
            self.command_func(args[1:])

class IntArgCommand(Command):
    """Overriden Command that passes an Integer argument to its callable function."""
    async def call(self, args: list[str]):
        if len(args) < 2:
            raise self.UsageError(f"{self.alias} expects an argument")

        index = args[1]

        try:
            index = int(index)
        except ValueError:
            raise self.UsageError(f"{self.alias} argument must be integer")
        
        if(iscoroutinefunction(self.command_func)):
            await self.command_func(index)
        else:
            self.command_func(index)
        

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
            except Command.UsageError as e:
                print(f"Usage Error: {e.args[0]}")

