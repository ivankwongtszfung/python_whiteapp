VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

run: $(VENV)/bin/activate
	$(PYTHON) main.py

setup: $(VENV)/bin/activate
	echo "activate the virtualenv with . $(VENV)/bin/activate"

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
	mkdir logs


clean:
	rm -rf __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf ./logs
	rm -rf $(VENV)