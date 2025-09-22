init:
	@uv sync

check:
	uv run tox -e black,ruff,mypy -p 3

test:
	uv run tox -e {{ cookiecutter.__pytest_target }}

ci:
	uv run tox -e black,ruff,mypy,{{ cookiecutter.__pytest_target }} -p 4

dev:
	uv run pip install --editable .

install:
	pip install .

.PHONY: init check test ci dev install
