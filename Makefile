.PHONY: test
test:
	@pipenv run test

.PHONY: init
init:
	@pipenv install --dev

.PHONY: ci
ci:
	@circleci local execute --job build-and-test
