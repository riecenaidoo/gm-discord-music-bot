"""The console controls for the Discord bot are managed by this module.

TODO: Testing, Documentation, Singleton Implementation of Console.
"""




class Command:

	def __init__(self, nameMatch:str):
		self.nameMatch = nameMatch
		self.func = None


	def set_action(action: callable):
		self.func = func


	def match(arg:str) -> bool:
		return (arg == nameMatch)


	def call(args:list(str)):
		self.func(args)

	

class Console:

	def __init__(self):
		self.commands = list()


	def add_command(command:Command):
		self.commands.append(command)


	def get_input() -> list(str):
		instruction = ""
		while len(instruction) == 0:
			instruction = input(" > ")

		return instruction.split(" ")


	def handle_command(args: list(str)):
		"""TODO: Raise exceptions"""

		for cmd in self.commands:
			if cmd.match(args[0]):
				cmd.call(args)
				break
		else:
			print("No match")


	def run():
		"""TODO: Catch exceptions, end loop, display messages."""

		while True:
			handle_command(get_input())


if __name__ == '__main__':
	console = Console()

	play = Command("play")
	play.set_action(lambda: print("play"))
	console.add_command(play)

	volume = Command("volume")
	def vol(args: list(str)):
		if len(args) < 1:
			raise UsageError("volume expects an argument")

		volume = args[1]

		try:
			volume = int(volume)
		except ValueError:
			raise UsageError("volume argument must be integer")

		if volume < 0 or volume > 100:
			raise UsageError("volume must be between 0 & 100")

		print("[VOLUME]")

	volume.set_action(vol)


	console.run()