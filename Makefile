HERE = $(shell pwd)
BIN = $(HERE)/bin
TESTS ?= genc
CIRCLECI ?= false

ifeq ($(TESTS), genc)
	TEST_ARG = genc --with-coverage --cover-package genc --cover-erase
else
	TEST_ARG = --tests=$(TESTS)
endif

ifeq ($(CIRCLECI), true)
PYTHON_VERSION = $(shell python -c "import sys; print('.'.join([str(s) for s in sys.version_info][:2]))")
PYTHON_2 = yes
ifeq ($(findstring 3.,$(PYTHON_VERSION)), 3.)
	PYTHON_2 = no
endif
endif

INSTALL = $(BIN)/pip install --no-deps --disable-pip-version-check

.PHONY: all build clean data python test

all: build

python:
ifeq ($(CIRCLECI), true)
ifeq ("$(PYTHON_2)", "yes")
	python -m virtualenv .
else
	python -m venv .
endif
endif

build: python
ifeq ($(CIRCLECI), true)
	$(INSTALL) -r requirements/test.txt
	python setup.py develop
endif

data:
	python3.6 build.py "data/GENC Standard XML Ed3.0.zip"

test:
ifeq ($(CIRCLECI), true)
	$(BIN)/nosetests -s -d -v $(TEST_ARG)
else
	circleci build --job python-2.7
	circleci build --job python-3.5
	circleci build --job python-3.6
endif
