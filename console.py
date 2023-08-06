"""The console controls for the Discord bot are managed by this module.

TODO: Testing, Documentation, Singleton Implementation of Console.
"""


class Command:

    def __init__(self, name_match: str):
        self.name_match = name_match.strip().casefold()
        self.func = None

    def set_action(self, action: callable):
        self.func = action

    def match(self, arg: str) -> bool:
        return arg.strip().casefold() == self.name_match

    def call(self, args: list[str]):
        self.func(args)


def get_input() -> list[str]:
    instruction = ""
    while len(instruction) == 0:
        instruction = input(" > ")

    return instruction.split(" ")


class Console:

    def __init__(self):
        self.commands = list()

    def add_command(self, command: Command):
        self.commands.append(command)

    def handle_command(self, args: list[str]):
        """TODO: Raise exceptions"""

        for cmd in self.commands:
            if cmd.match(args[0]):
                cmd.call(args)
                break
        else:
            print("No match")

    def run(self):
        """TODO: Catch exceptions, end loop, display messages."""

        while True:
            try:
                self.handle_command(get_input())
            except UsageError as e:
                print(f"Usage Error: {e.args[0]}")


class UsageError(Exception):
    pass


if __name__ == '__main__':
    console = Console()

    play_cmd = Command("play")
    play_cmd.set_action(lambda args: print("[PLAY]"))
    console.add_command(play_cmd)

    volume_cmd = Command("volume")


    def vol(args: list[str]):
        if len(args) < 2:
            raise UsageError("volume expects an argument")

        volume = args[1]

        try:
            volume = int(volume)
        except ValueError:
            raise UsageError("volume argument must be integer")

        if volume < 0 or volume > 100:
            raise UsageError("volume must be between 0 & 100")

        print("[VOLUME]")


    volume_cmd.set_action(vol)
    console.add_command(volume_cmd)

    console.run()
