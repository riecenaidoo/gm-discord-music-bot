PYTHON_HOME = python3
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip


.PHONY: run help clean


$(VENV)/bin/activate: requirements.txt
	$(PYTHON_HOME) -m venv $(VENV)
	$(PIP) install -r requirements.txt


run: ARGS?=
run: $(VENV)/bin/activate
	$(PYTHON) main.py $(ARGS)


help: $(VENV)/bin/activate
	@echo "\n---------------------------------------"
	@echo "Makefile Help:"
	@echo "---------------------------------------"
	@echo "make run \t\t\t<--- Start the Bot service with default settings."
	@echo "make run ARGS=\"\" \t\t<--- Pass more specific arguments to the Bot service."
		@echo "\te.g. ARGS=\"-n 'localhost' -p 5001 -t '12345BotToken!'\"\n"
	@echo "---------------------------------------"
	@echo "Script Args:"
	@echo "---------------------------------------"
	@$(PYTHON) main.py -h
	@echo "---------------------------------------\n"


clean:
	rm -rf __pycache__
	rm -rf $(VENV)
