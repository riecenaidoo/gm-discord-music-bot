PYTHON_HOME = python3
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
RUFF = $(VENV)/bin/ruff
MAIN = src/main.py



$(VENV)/bin/activate: requirements.txt
	$(PYTHON_HOME) -m venv $(VENV)
	$(PIP) install -r requirements.txt


.PHONY: run
run: ARGS?=
run: $(VENV)/bin/activate
	$(PYTHON) $(MAIN) $(ARGS)


.PHONY: help
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
	@$(PYTHON) $(MAIN) -h
	@echo "---------------------------------------\n"


# Check before push.
.PHONY:check
check: $(VENV)/bin/activate tools.txt
	$(PIP) install -r tools.txt
	$(RUFF) format src/
	$(RUFF) check src/ --fix


.PHONY:clean
clean:
	rm -rf src/__pycache__
	rm -rf src/bot/__pycache__
	rm -rf .ruff_cache
	rm -rf $(VENV)
