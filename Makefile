PYTHON_HOME = python3
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip


.PHONY: run help clean


$(VENV)/bin/activate: requirements.txt
	$(PYTHON_HOME) -m venv $(VENV)
	$(PIP) install -r requirements.txt


run: HOST?=
run: PORT?=
run: $(VENV)/bin/activate
	$(PYTHON) main.py


help: $(VENV)/bin/activate
	$(PYTHON) main.py -h


mock: SHELL:= /bin/bash	# Specifically only on Bash.
mock: HOST?=
mock: PORT?=
mock:
	@if ! test -z "$$HOST" && ! test -z "$$PORT";\
		then echo "Set Both";\
	elif ! test -z "$$HOST";\
		then echo "Just host";\
	elif ! test -z "$$PORT";\
		then echo "Just port";\
	else echo "neither";\
	\
	fi;

clean:
	rm -rf __pycache__
	rm -rf $(VENV)
