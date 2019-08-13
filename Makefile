all: test black flake8

test:
	pytest

black:
	black --check bin lib

flake8:
	flake8 bin lib
