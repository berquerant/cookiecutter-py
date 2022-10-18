.PHONY: ci
ci:
	@pipenv run ci

.PHONY: fix
fix:
	@pipenv run ist
	@pipenv run fmt

.PHONY: clean
clean:
	@rm -rf build dist .pytest_cache .tox
	@find . -name "*.egg" -exec rm -rf {} +
	@find . -name "*.egg-info" -exec rm -rf {} +
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -exec rm -rf {} +

.PHONY: dev
dev:
	@pipenv run dev

.PHONY: install
install: clean
	@pipenv run install

.PHONY: dist
dist: clean
	@pipenv run dist
	@ls -al dist

.PHONY: init
init:
	@pipenv install --dev
