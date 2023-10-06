PYTHON_HOME = python3
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip


.PHONY: run help clean


$(VENV)/bin/activate: requirements.txt
	$(PYTHON_HOME) -m venv $(VENV)
	$(PIP) install -r requirements.txt


run: SHELL:= /bin/bash	# Specifically only on Bash.
run: HOST?=
run: PORT?=
run: $(VENV)/bin/activate
	@if ! test -z "$$HOST" && ! test -z "$$PORT";\
		then $(PYTHON) main.py --HOSTNAME=$(HOST) --PORT=$(PORT);\
	elif ! test -z "$$HOST";\
		then $(PYTHON) main.py --HOSTNAME=$(HOST);\
	elif ! test -z "$$PORT";\
		then $(PYTHON) main.py --PORT=$(PORT);\
	else $(PYTHON) main.py;\
	\
	fi;


help: $(VENV)/bin/activate
	@echo "---------------------------------------"
	@echo "Script Args:"
	@echo "---------------------------------------"
	@$(PYTHON) main.py -h
	@echo "---------------------------------------"
	@echo "Try: make run HOST=\"...\" PORT=..."
	@echo "---------------------------------------"


clean:
	rm -rf __pycache__
	rm -rf $(VENV)
