VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

.PHONY: run clean


run: $(VENV)/bin/activate
	$(PYTHON) main.py


venv/bin/activate: requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --no-cache-dir -r requirements.txt


clean:
	rm -rf __pycache__
	rm -rf $(VENV)
