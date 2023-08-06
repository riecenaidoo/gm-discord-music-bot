"""The console controls for the Discord bot are managed by this module.

TODO: Testing, Documentation, Singleton Implementation of Console.
"""



def class Command:

	def __init__(self, nameMatch:str):
		self.nameMatch = nameMatch
		self.func = None


	def set_action(action:func):
		self.func = func


	def match(arg:str) -> bool:
		return (arg == nameMatch)


	def call(args:str[]):
		self.func(args)


def class Console:

	def __init__(self):
		self.commands = list()


	def add_command(command:Command):
		self.commands.append(command)


	def get_input() -> str[]:
		instruction = ""
		while len(instruction) == 0:
			instruction = input(" > ")

		return instruction.split(" ")


	def handle_command(args:str[]):
		"""TODO: Raise exceptions"""

		for(Command cmd: self.commands):
			if cmd.match(args[0]):
				cmd.call(args)
				break
		else:
			print("No match")


	def run():
		"""TODO: Catch exceptions, end loop, display messages."""

		while True:
			handle_command(get_input())