"""Asynchronous console controls for the Discord bot are managed by this module."""

import logging
from inspect import iscoroutinefunction

import utils
from bot.music_client import MusicClient


_log = logging.getLogger(__name__)
_log.addHandler(utils.HANDLER)
_log.setLevel(logging.WARNING)


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
            args (list[str]): Placeholder for arguments to be passed to a callable func. 
            Used when call is overriden by inheritors.
        """
        _log.debug("Ignoring unnessary args %s", args)
        if iscoroutinefunction(self.command_func):
            await self.command_func()
        else:
            self.command_func()

    class UsageError(Exception):
        """Raised by an extended Command if the additional arguments received
        for the Command were invalid.
        """


class StringArgsCommand(Command):
    """Extended Command that passes many string args to its callable function."""
    async def call(self, args: list[str]):
        if len(args) < 2:
            raise self.UsageError("Expects atleast one argument")

        if iscoroutinefunction(self.command_func):
            await self.command_func(args[1:])
        else:
            self.command_func(args[1:])


class IntArgCommand(Command):
    """Extended Command that passes an Integer argument to its callable function."""
    async def call(self, args: list[str]):
        if len(args) != 2:
            raise self.UsageError("Expects one argument")

        index = args[1]

        try:
            index = int(index)
        except ValueError as exc:
            raise self.UsageError("Argument must be an Integer") from exc
        if iscoroutinefunction(self.command_func):
            await self.command_func(index)
        else:
            self.command_func(index)


class Console:
    """Console..."""

    def __init__(self):
        """Init..."""
        self.commands: list[Command] = list()
        self.online: bool = True

    def add_command(self, command: Command):
        """Adds a Command this Console can support matching against.

        To prevent duplication, this method will not add a Command 
        if its alias matches an existing Command in this Console.

        Args:
            command (Command): Command to add.
        """

        for cmd in self.commands:
            if cmd.match(command.alias):
                _log.warning(
                    "Console already has a Command with the alias '%s'.", command.alias)
                return
        self.commands.append(command)

    async def handle_command(self, args: list[str]):
        """Calls the appropriate Command from this Console, if any.

        Args:
            args (list[str]): A list of arguments for the Command, 
            where args[0] is the alias of the Command requested.
        """

        for cmd in self.commands:
            if cmd.match(args[0]):
                await cmd.call(args)
                return
        _log.warning("Command '%s' is not supported.", args[0])

    async def start(self, input_method: callable):
        """Continously receives input and calls Commands
        as they are matched.
        """

        get_input = utils.to_thread(input_method)
        while self.online:
            try:
                command = await get_input()
                await self.handle_command(command)
            except Command.UsageError as e:
                _log.warning("Command %s Usage Error: '%s'.",
                             command[0].upper(), e.args[0])


def __build_console_commands(console: Console, client: MusicClient):
    """Builds the Commands to control a MusicClient to this Console.

    Args:
        console (Console): Console to add Commands to.
        client (MusicClient): MusicClient this Console should control. 
    """
    # Voice Channel Controls
    console.add_command(Command("channels", client.get_voice_channels))
    console.add_command(IntArgCommand("join", client.voice_join))
    console.add_command(Command("leave", client.voice_leave))
    # Audio Controls
    console.add_command(Command("pause", client.audio_pause))
    console.add_command(Command("resume", client.audio_resume))
    console.add_command(IntArgCommand("volume", client.set_audio_volume))
    # Song Controls
    console.add_command(Command("skip", client.song_skip))
    console.add_command(Command("prev", client.song_prev))
    # Playlist Controls
    console.add_command(StringArgsCommand("queue", client.playlist_queue))
    console.add_command(Command("start", client.playlist_start))
    console.add_command(Command("stop", client.playlist_stop))
    console.add_command(Command("clear", client.playlist.clear))
    console.add_command(StringArgsCommand("play", client.playlist_play))
    # Playlist Mode Controls
    console.add_command(Command("shuffle", client.playlist.shuffle_mode))
    console.add_command(Command("loop", client.playlist.loop_mode))
    console.add_command(Command("repeat", client.playlist.repeat_mode))
    console.add_command(Command("normal", client.playlist.no_looping_mode))


def build_console(client: MusicClient) -> Console:
    """Builds a Console for this MusicClient.

    Args:
        client (MusicClient): MusicClient for this Console to control.

    Returns:
        Console: Console that can control this MusicClient.
    """

    console = Console()
    __build_console_commands(console, client)
    return console
