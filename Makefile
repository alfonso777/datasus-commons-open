# Makefile
# 
# > make help
#
# The following commands can be used.
#
# init:  sets up environment and installs requirements
# install:  Installs development requirements
# clean:  Remove build and cache files
# env:  Source venv and environment files for testing
# leave:  Cleanup and deactivate venv
# test:  Run pytest
# run:  Executes

VENV_PATH='env/bin/activate'
#ENVIRONMENT_VARIABLE_FILE='.env'

define find.functions
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
endef

help:
	@echo 'The following commands can be used.'
	@echo ''
	$(call find.functions)

init: ## sets up environment and installs requirements
init:
	pip install setuptools wheel twine

install: ## Installs development requirments
install:
	# Installing DBC conversion
	mkdir -p tmpinstalls/
	[[ -d  tmpinstalls/blast-dbf ]] || (cd tmpinstalls && git clone https://github.com/eaglebh/blast-dbf.git )
	cd tmpinstalls/blast-dbf && make
	#rm -r tmpinstalls/blast-dbf

	#python -m pip install --upgrade pip
	# Used for packaging and publishing
	pip install -r requirements.txt
	
package: ## Create package in dist
package: clean
	python setup.py sdist bdist_wheel

upload-test: ## Create package and upload to test.pypi
upload-test: package
	python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/* --non-interactive --verbose

upload: ## Create package and upload to pypi
upload: package
	python -m twine upload dist/* --non-interactive

clean: ## Remove build and cache files
clean:
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist
	rm -rf .pytest_cache
	# Remove all pycache
	find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

env: ## Source venv and environment files for testing
env:
	python -m venv env
	source $(VENV_PATH)
	#source $(ENVIRONMENT_VARIABLE_FILE)

leave: ## Cleanup and deactivate venv
leave: clean
	deactivate

test: ## Run pytest
test:
	pytest . -p no:logging -p no:warnings
