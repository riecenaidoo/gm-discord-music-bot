"""Asynchronous console controls for the Discord bot are managed by this module."""
import asyncio
import functools
import typing
from inspect import iscoroutinefunction
import logging
import utils



_log = logging.getLogger(__name__)
_log.addHandler(utils.HANDLER)
_log.setLevel(logging.WARNING)


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
    """Extended Command that passes many string args to its callable function."""
    async def call(self, args: list[str]):
        if len(args) < 2:
            raise self.UsageError(f"Expects atleast one argument")

        if(iscoroutinefunction(self.command_func)):
            await self.command_func(args[1:])
        else:
            self.command_func(args[1:])

class IntArgCommand(Command):
    """Extended Command that passes an Integer argument to its callable function."""
    async def call(self, args: list[str]):
        if len(args) != 2:
            raise self.UsageError(f"Expects one argument")

        index = args[1]

        try:
            index = int(index)
        except ValueError:
            raise self.UsageError(f"Argument must be an Integer")
        
        if(iscoroutinefunction(self.command_func)):
            await self.command_func(index)
        else:
            self.command_func(index)
        

class Console:

    def __init__(self):
        self.COMMANDS:list[Command] = list()
        self.online:bool = True

    def add_command(self, command: Command):
        """Adds a Command this Console can support matching against.
        
        To prevent duplication, this method will not add a Command 
        if its alias matches an existing Command in this Console.
        
        Args:
            command (Command): Command to add.
        """
        for cmd in self.COMMANDS:
            if cmd.match(command.alias):
                _log.warning(f"Console already has a Command with the alias '{command.alias}'.")
                return
        self.COMMANDS.append(command)

    async def handle_command(self, args: list[str]):
        """Calls the appropriate Command from this Console, if any.

        Args:
            args (list[str]): A list of arguments for the Command, where args[0] is the alias of the Command requested.
        """
        for cmd in self.COMMANDS:
            if cmd.match(args[0]):
                await cmd.call(args)
                return
        _log.warning(f"Command '{args[0]}' is not supported.")

    async def start(self, input_method: callable):
        """Continously receives input and calls Commands
        as they are matched.
        """
        
        get_input = to_thread(input_method)
        while self.online:
            try:
                command = await get_input()
                await self.handle_command(command)
            except Command.UsageError as e:
                _log.warning(f"Command {command[0].upper()} Usage Error: '{e.args[0]}'.")

