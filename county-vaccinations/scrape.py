"""
Download the COVID vaccination rates by county.

Source: https://github.com/datadesk/california-coronavirus-data
"""
import pathlib
import pandas as pd

# Pathing
THIS_DIR = pathlib.Path(__file__).parent.absolute()
DATA_DIR = THIS_DIR / "data"

def write_quarterly_csv(df, quarter):
    fields = [
        'date',
        'county',
        'at_least_one_dose',
        'fully_vaccinated',
        'new_doses_administered',
        'weekly_new_doses'
    ]
    df[fields].to_csv(
        DATA_DIR / "{}.csv".format(quarter),
        index=False,
        na_rep='N',
        float_format='%.0f'
    )


def process_county(group):
    g = group.sort_values('date').set_index('date')
    g_sum = g.resample('D').asfreq().rolling(7).sum()
    g['weekly_new_doses'] = g_sum['new_doses_administered']
    return g.drop(['county'], axis='columns')


def main():
    """
    Download the data and split
    """
    # Download the data

    url = 'https://raw.githubusercontent.com/datadesk/california-coronavirus-data/master/cdph-vaccination-county-totals.csv';
    df = pd.read_csv(url)

    df['date'] = pd.to_datetime(df['date'])

    df = df[['date', 'county', 'at_least_one_dose', 'fully_vaccinated', 'new_doses_administered']]
    df = df.groupby('county').apply(process_county).reset_index()

    df['year'] = df['date'].dt.year.astype(str)
    df['quarter'] = df['date'].dt.quarter.astype(str)
    df['year_quarter'] = df[['year', 'quarter']].agg('-'.join, axis=1)

    grouped_by_quarter = df.groupby('year_quarter')
    quarters = grouped_by_quarter.groups.keys()

    for quarter in grouped_by_quarter.groups.keys():
        quarter_df = grouped_by_quarter.get_group(quarter)
        write_quarterly_csv(quarter_df, quarter)


if __name__ == '__main__':
    main()
