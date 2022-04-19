"""
Derive the prison points from the LA Times Datadesk dataset on COVID in prisons.

Source: https://github.com/datadesk/california-coronavirus-data
"""
import geojson
import pathlib
import pandas as pd

# Pathing
THIS_DIR = pathlib.Path(__file__).parent.absolute()
DATA_DIR = THIS_DIR / "data"

def main():
    df = pd.read_csv('https://raw.githubusercontent.com/datadesk/california-coronavirus-data/master/cdcr-prison-totals.csv')
    
    by_prison = df.groupby('code').first().reset_index()
    by_prison = by_prison[['code', 'name', 'city', 'county', 'fips', 'zipcode', 'x', 'y']]
    features = []
    for index, row in by_prison.iterrows():
        properties = row.to_dict()
        properties.pop('x', None)
        properties.pop('y', None)
        features.append(geojson.Feature(
            geometry=geojson.Point((row['x'], row['y'])),
            properties=row.to_dict()
        ))
    feature_collection = geojson.FeatureCollection(features)

    with open(DATA_DIR / "covid-prisons.geojson", 'w') as outfile:
        geojson.dump(feature_collection, outfile)


if __name__ == '__main__':
    main()
