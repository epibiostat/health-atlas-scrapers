"""
Download the COVID vaccine equity metric.

Source: https://data.ca.gov/dataset/covid-19-vaccine-progress-dashboard-data-by-zip-code/resource/15702a90-aa5d-49bc-8621-a8129630725a
"""
import json
import pathlib
import pandas as pd
import urllib.request

# Pathing
THIS_DIR = pathlib.Path(__file__).parent.absolute()
DATA_DIR = THIS_DIR / "data"

RESOURCE_ID = '15702a90-aa5d-49bc-8621-a8129630725a'

def write_csv(df):
    fields = ['zcta', 'vaccine_equity_metric_quartile']
    df[fields].to_csv(
        DATA_DIR / "latest.csv",
        index=False,
        na_rep='N',
        float_format='%.0f'
    )


def get_latest_date():
    """
    Get latest available date
    """
    url = "https://data.ca.gov/api/3/action/datastore_search?resource_id={}&sort=as_of_date%20desc&limit=1".format(RESOURCE_ID)
    with urllib.request.urlopen(url) as request:
        data = json.loads(request.read().decode())
        return data['result']['records'][0]['as_of_date']


def get_data_for_date(date):
    sql = 'SELECT zip_code_tabulation_area, vaccine_equity_metric_quartile FROM "{}" WHERE "as_of_date" = \'{}\''.format(RESOURCE_ID, date)
    url = "https://data.ca.gov/api/3/action/datastore_search_sql?sql={}".format(urllib.request.pathname2url(sql))
    with urllib.request.urlopen(url) as request:
        data = json.loads(request.read().decode())
        return data['result']['records']


def main():
    """
    Download the data and split
    """
    # Download the data

    latest_date = get_latest_date()

    df = pd.DataFrame(get_data_for_date(latest_date)) \
            .rename(columns={ 'zip_code_tabulation_area': 'zcta' })

    write_csv(df)


if __name__ == '__main__':
    main()
