# health-atlas-scrapers

Data scrapers and preprocessing for Health Atlas.

Much of the approach to this is borrowed from [datadesk/california-coronavirus-scrapers](https://github.com/datadesk/california-coronavirus-scrapers).

## Installation

Clone the repo, then install dependencies:

```
pipenv install
```

To run all of the scrapers run:

```
make
```

To run a single scraper run (for example):

```
make -f county-cases/Makefile
```
