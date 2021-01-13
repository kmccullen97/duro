PY=python3

run:
	ENV=dev $(PY) -m duro

lint:
	$(PY) -m flake8 .

g-docs:
	$(PY) scripts/generate_command_docs.py
	$(PY) scripts/generate_default_config.py

.PHONY: build
build:
	$(PY) setup.py sdist bdist_wheel
