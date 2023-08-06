"""Asynchronous console controls for the Discord bot are managed by this module."""


class Command:

    def __init__(self, name_match: str, action_func: callable):
        self.name_match = name_match.strip().casefold()
        self.action_func = action_func

    def match(self, arg: str) -> bool:
        return arg.strip().casefold() == self.name_match

    async def call(self, args: list[str]):
        await self.action_func()


class PlayCommand(Command):

    async def call(self, args: list[str]):
        if len(args) < 2:
            raise UsageError(f"{self.name_match} expects an argument")

        await self.action_func(args[1])


class VolumeCommand(Command):

    async def call(self, args: list[str]):
        if len(args) < 2:
            raise UsageError(f"{self.name_match} expects an argument")

        volume = args[1]

        try:
            volume = int(volume)
        except ValueError:
            raise UsageError("volume argument must be integer")

        if volume < 0 or volume > 100:
            raise UsageError("volume must be between 0 & 100")

        await self.action_func(volume)


class Console:

    def __init__(self, input_method: callable):
        self.commands = list()
        self.input_method = input_method
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
                await self.handle_command(self.input_method())
            except UsageError as e:
                print(f"Usage Error: {e.args[0]}")


class UsageError(Exception):
    pass
