init:
	@uv sync

test:
	@uv run pytest -s -v --ff --doctest-modules tests

.PHONY: init test
