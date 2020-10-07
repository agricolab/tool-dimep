SHELL := /bin/bash #to be able to execute `source`

.PHONY: build docs clean test upload

build: clean
	python setup.py  sdist bdist_wheel
	

docs:
	rm -rf docs/build/html
	rm -rf docs/build/doctree
	rm -rf docs/source/_autosummary
	if [ ! -d docs/source/_static ] ; then mkdir docs/source/_static; fi
	make -C docs html

clean:
	rm -rf dist */*.egg-info *.egg-info  build
	rm -rf .test

test: build
	test/runtest

upload: build
	twine check dist/*
	twine upload dist/* --verbose