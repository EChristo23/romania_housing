import pandas as pd
import sqlalchemy as db
import os

labs = {
    'price': 'Price (\N{euro sign})',
    'suprafata_utila': 'Net Area (m\u00b2)',
    'price_per_sqmeter': 'Price (\N{euro sign}) per net m\u00b2',
    'probability':  'Proportion',
    'property_type': 'Property Type',
    'zona': 'Region/Zona'
}

var_names = {
    'price': 'price',
    'suprafata_utila': 'net area',
    'price_per_sqmeter': 'price per net square meter'
}

units = {
    'price': '\N{euro sign}',
    'suprafata_utila': 'm\u00b2',
    'price_per_sqmeter': '\N{euro sign}/ m\u00b2'
}
custom_data = ["id", 'property_type', 'zona', 'price_per_sqmeter', 'price', 'suprafata_utila', 'url']

attributes_dict = dict(zip(custom_data, range(len(custom_data))))


def get_custom_data_index(attribute_name: str):
    return attributes_dict.get(attribute_name)


def get_data():
    uri = os.environ.get('URI')
    if uri:
        engine = db.create_engine(uri)
        df = pd.read_sql_table(table_name='df_input', con=engine)
        return df
    else:
        df = pd.read_pickle('./data/df_input.pkl')
        return df