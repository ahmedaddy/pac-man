PYTHON = python
MAIN = main
CONFIG_FILE = config.json

install:
		pip install -r requirements.txt

run:
		$(PYTHON) -m src.$(MAIN) $(CONFIG_FILE)

debug:
		$(PYTHON) -m pudb $(MAIN) $(CONFIG_FILE)

clean:
		find . -type d -name "__pycache__" -exec rm -rf {} +
		rm -rf .mypy_cache

lint:
		flake8 .
		mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs