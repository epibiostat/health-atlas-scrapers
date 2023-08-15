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
    fields = ['date', 'county', 'cases', 'deaths', 'new_cases', 'new_deaths']
    df[fields].to_csv(
        DATA_DIR / "{}.csv".format(quarter),
        index=False,
        na_rep='N',
        float_format='%.0f'
    )


def write_state_csv(df):
    fields = ['date', 'cases', 'deaths', 'new_cases', 'new_deaths']
    df.groupby('date').sum().reset_index()[fields].to_csv(DATA_DIR / "state-cases.csv", index=False)


def process_county(group):
    g = group.sort_values('date').set_index('date')
    g_sum = g.resample('D').sum()

    g_diff = g_sum.diff(periods=7)

    g_sum['new_cases'] = g_diff['cases']
    g_sum['new_deaths'] = g_diff['deaths']
    return g_sum


def main():
    """
    Download the county cases data and split
    """
    # Download the data
    url = "https://raw.githubusercontent.com/datadesk/california-coronavirus-data/master/cdph-county-cases-deaths.csv"
    df = pd.read_csv(url)

    df = df[['date', 'county', 'confirmed_cases', 'confirmed_deaths']] \
            .rename(columns={
                'confirmed_cases': 'cases',
                'confirmed_deaths': 'deaths',
            })

    df['date'] = pd.to_datetime(df['date'])

    df = df.groupby('county').apply(process_county).reset_index()

    df['year'] = df['date'].dt.year.astype(str)
    df['quarter'] = df['date'].dt.quarter.astype(str)
    df['year_quarter'] = df[['year', 'quarter']].agg('-'.join, axis=1)

    grouped_by_quarter = df.groupby('year_quarter')
    quarters = grouped_by_quarter.groups.keys()

    for quarter in grouped_by_quarter.groups.keys():
        quarter_df = grouped_by_quarter.get_group(quarter)
        write_quarterly_csv(quarter_df, quarter)

    write_state_csv(df)


if __name__ == '__main__':
    main()
