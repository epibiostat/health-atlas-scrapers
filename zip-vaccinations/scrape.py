"""
Download the COVID vaccination rates by zip code.

Source: https://github.com/datadesk/california-coronavirus-data
"""
import pathlib
import pandas as pd

# Pathing
THIS_DIR = pathlib.Path(__file__).parent.absolute()
DATA_DIR = THIS_DIR / "data"

def write_quarterly_csv(df, quarter):
    fields = ['date', 'zcta', 'at_least_one_dose', 'fully_vaccinated']
    df[fields].to_csv(
        DATA_DIR / "{}.csv".format(quarter),
        index=False,
        na_rep='N',
        float_format='%.0f'
    )


def process_zip(group):
    g = group.sort_values('date')

    # Find possible quarters for this date range
    quarters = pd.date_range(start=g['date'].min(), end=g['date'].max(), freq='QS')
    quarters = [q for q in quarters if g[g['date'] == q].empty]
    quarters_df = pd.DataFrame(data={'date': quarters})
    quarters_df = quarters_df.set_index(['date'])

    # Add empty rows for the start of each quarter and pad with previous data
    g = g.set_index(['date'])
    g = pd.concat([g, quarters_df]).sort_values(by='date')
    g = g.pad()

    return g.drop(['zcta'], axis='columns')


def main():
    """
    Download the data and split
    """
    # Download the data

    url = 'https://raw.githubusercontent.com/datadesk/california-coronavirus-data/master/cdph-vaccination-zipcode-totals.csv';
    df = pd.read_csv(url)

    df = df[['date', 'id', 'at_least_one_dose', 'fully_vaccinated']]

    df['zcta'] = df['id'].astype(str)
    df['date'] = pd.to_datetime(df['date'])

    df = df[['date', 'zcta', 'at_least_one_dose', 'fully_vaccinated']]
    df = df.groupby('zcta').apply(process_zip).reset_index()

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
