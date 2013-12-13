setup:
	virtualenv venv
	venv/bin/pip install -r requirements.txt

test:
	PYTHONPATH=$(shell pwd) venv/bin/python rob/tests.py
	flake8
