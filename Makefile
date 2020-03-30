all: test black flake8
	@echo "🚀😀👌😍🚀"

test:
	pytest

black:
	black --check bin lib

flake8:
	flake8 bin lib
