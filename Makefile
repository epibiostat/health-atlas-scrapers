# Import global variables
include ./utils/variables.make

all: scrape          \
     clean_notebooks


scrape: ## Verify that our notebooks can be parsed and run. Example: make scrape
	$(call make,county-cases/Makefile)
	$(call make,zip-vaccinations/Makefile)


clean_notebooks: ## Remove all temporary notebook outputs created by the our commands. Example: make clean_notebooks
	@find . -type f -name '*-output.ipynb' -delete


lint_notebooks: ## Verify that our notebooks can be parsed and run. Example: make lint_notebooks
	@pipenv run jupyter nbconvert ./**/*.ipynb --to=html --stdout > /dev/null


lint_python:
	@pipenv run flake8 ./

help: ## Show this help. Example: make help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


# Mark all the command that don't have a target
.PHONY: all             \
        scrape          \
        lint_notebooks  \
        help
