"""
Download the COVID cases and death data by country from LA Times Datadesk.

Source: https://github.com/datadesk/california-coronavirus-data
"""
import pathlib
import pandas as pd

# Pathing
THIS_DIR = pathlib.Path(__file__).parent.absolute()
DATA_DIR = THIS_DIR / "data"


def write_quarterly_csv(df, quarter):
    fields = ['date', 'county', 'confirmed_cases', 'reported_deaths']
    df[fields].to_csv(DATA_DIR / "county-cases-{}.csv".format(quarter), index=False)


def write_state_csv(df):
    fields = ['date', 'confirmed_cases', 'reported_deaths']
    df.groupby('date').sum().reset_index()[fields].to_csv(DATA_DIR / "state-cases.csv", index=False)


def main():
    """
    Download the county cases data and split
    """
    # Download the data
    url = "https://raw.githubusercontent.com/datadesk/california-coronavirus-data/master/cdph-county-cases-deaths.csv"
    df = pd.read_csv(url)

    df['date_obj'] = pd.to_datetime(df['date'])
    df['year'] = df['date_obj'].dt.year.astype(str)
    df['quarter'] = df['date_obj'].dt.quarter.astype(str)

    df['year_quarter'] = df[['year', 'quarter']].agg('-'.join, axis=1)

    grouped_by_quarter = df.groupby('year_quarter')
    quarters = grouped_by_quarter.groups.keys()

    for quarter in grouped_by_quarter.groups.keys():
        quarter_df = grouped_by_quarter.get_group(quarter)
        write_quarterly_csv(quarter_df, quarter)

    write_state_csv(df)


if __name__ == '__main__':
    main()
