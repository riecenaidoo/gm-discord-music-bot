PYTHON_HOME = python3
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip


.PHONY: run clean


run: $(VENV)/bin/activate
	$(PYTHON) main.py


$(VENV)/bin/activate: requirements.txt
	$(PYTHON_HOME) -m venv $(VENV)
	$(PIP) install -r requirements.txt


clean:
	rm -rf __pycache__
	rm -rf $(VENV)
