# Import aliases
include ./utils/variables.make

MAKENAME = prison-cases

scrape: ## Scrape data files. Example: make -f ./prison-cases/Makefile
	$(call start,$(MAKENAME))
	$(call python,./prison-cases/scrape.py)
	$(call finish)

help: ## Show this help. Example: make -f ./prison-cases/Makefile help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Mark commands without a target
.PHONY: scrape help
