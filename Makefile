VERSION := 1.0.1

build:
	python3 setup.py build

clean:
	rm -rf build dist eljef_core.egg-info \
		eljef/__pycache__ eljef/backup/__pycache__  eljef/backup/plugins/__pycache__ \
		tests/__pycache__ tests/_trial_temp \
		.pytest_cache .coverage

depsinstall:
	pip install -r requirements.txt

depsupdate:
	pip install --upgrade -r requirements.txt

install:
	python3 setup.py install

lint:
	flake8 eljef/core
	pylint eljef/core

test:
	pytest

testcoverage:
	pytest --cov=eljef/ tests/

versionget:
	@echo $(VERSION)

versionset:
	@$(eval OLDVERSION=$(shell cat setup.py | awk -F"[=,]" '/version=/{gsub("\047", ""); print $$2}'))
	@sed -i -e "s/$(OLDVERSION)/$(VERSION)/" eljef/core/__version__.py
	@sed -i -e "s/version = '$(OLDVERSION)'/version = '$(VERSION)'/" \
	        -e "s/release = '$(OLDVERSION)'/release = '$(VERSION)'/" docs/source/conf.py
	@sed -i -e "s/version='$(OLDVERSION)'/version='$(VERSION)'/" setup.py
