PYTHON := pipenv run python -W ignore
JUPYTER := $(PYTHON) ./utils/run.py

define python
    @echo "Executing Python script $(1)\r";
    @$(PYTHON) $(1)
endef

define jupyter
    @echo "Executing Jupyter notebook $(1)\r";
    @$(JUPYTER) $(1)
endef

define make
    @echo "Executing Makefile $(1)\r";
	$(call start,$(MAKENAME))
    @$(MAKE) --no-print-directory -f $(1)
endef
