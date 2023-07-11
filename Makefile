

.PHONY: run clean


venv/bin/activate: requirements.txt
	python3 -m venv venv
	./venv/bin/pip install --no-cache-dir -r requirements.txt


run: venv/bin/activate
	./venv/bin/python main.py


clean:
	rm -rf __pycache__
	rm -rf venv