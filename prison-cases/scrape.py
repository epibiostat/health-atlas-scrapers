"""
Get the prison data from the LA Times Datadesk dataset on COVID in prisons.

Source: https://github.com/datadesk/california-coronavirus-data
"""
import json
import pathlib
import pandas as pd

# Pathing
THIS_DIR = pathlib.Path(__file__).parent.absolute()
DATA_DIR = THIS_DIR / "data"


def main():
    df = pd.read_csv('https://raw.githubusercontent.com/datadesk/california-coronavirus-data/master/cdcr-prison-totals.csv')

    by_county = df.groupby(['county', 'date']).agg({
        'confirmed_cases': 'sum',
        'new_confirmed_cases': 'sum',
        'deaths': 'sum',
        'new_deaths': 'sum',
    }).reset_index()   

    by_county.to_csv(DATA_DIR / "covid-prison-data-by-county.csv", index=False)


if __name__ == '__main__':
    main()
