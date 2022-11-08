VERSION := 2022.10.2

build:
	python3 -m build --wheel --no-isolation

clean:
	rm -rf build dist eljef_backup.egg-info \
		eljef/__pycache__ eljef/backup/__pycache__  eljef/backup/plugins/__pycache__ \
		tests/__pycache__ tests/_trial_temp \
		.pytest_cache .coverage

depsinstall:
	pip install -r requirements.txt

depsupdate:
	pip install --upgrade -r requirements.txt

install:
	python3 -m installer dist/*.whl

lint:
	flake8 eljef/backup
	pylint eljef/backup

versionget:
	@echo $(VERSION)

versionset:
	@$(eval OLDVERSION=$(shell cat setup.py | awk -F"[=,]" '/version=/{gsub("\047", ""); print $$2}'))
	@sed -i -e "s/$(OLDVERSION)/$(VERSION)/" eljef/backup/__version__.py
	@sed -i -e "s/version='$(OLDVERSION)'/version='$(VERSION)'/" setup.py
