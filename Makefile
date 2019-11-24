all: isort yapf flake8

isort:
	isort -y -rc .

yapf:
	yapf -i -r .

flake8:
	flake8 .
