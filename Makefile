HERE = $(shell pwd)
BIN = $(HERE)/bin
TESTS ?= genc
TRAVIS ?= false

ifeq ($(TRAVIS), true)
	PYTHON = python
	PIP = pip
	NOSE = nosetests
else
	PYTHON = $(BIN)/python
	PIP = $(BIN)/pip
	NOSE = $(BIN)/nosetests
endif

ifeq ($(TESTS), genc)
	TEST_ARG = genc --with-coverage --cover-package genc --cover-erase
else
	TEST_ARG = --tests=$(TESTS)
endif

INSTALL = $(PIP) install --no-deps --disable-pip-version-check

BUILD_DIRS = .tox bin build dist include lib lib64 man share genc.egg-info

.PHONY: all build clean data test tox

all: build

$(PYTHON):
ifeq ($(TRAVIS), true)
	virtualenv .
else
	virtualenv-3.4 .
endif

build: $(PYTHON)
	$(INSTALL) -r requirements/test.txt
	$(PYTHON) setup.py develop

clean:
	rm -rf $(BUILD_DIRS)
	rm -f $(HERE)/.coverage

data:
	$(PYTHON) build.py "data/GENC Standard XML Ed3.0.zip"

test:
	$(NOSE) -s -d -v $(TEST_ARG)

tox:
	$(BIN)/tox
