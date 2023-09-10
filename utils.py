import pandas as pd
import sqlalchemy as db
import os

labs = {
    'price': 'Price (\N{euro sign})',
    'suprafata_utila': 'Net Area (m\u00b2)',
    'price_per_sqmeter': 'Price (\N{euro sign}) per net m\u00b2',
    'probability':  'Proportion',
    'property_type': 'Property Type',
    'county': 'County',
    'city': 'City'
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
custom_data = ["id", 'property_type', 'county',
               'price_per_sqmeter', 'price', 'suprafata_utila', 'url', 'city']

attributes_dict = dict(zip(custom_data, range(len(custom_data))))


def get_custom_data_index(attribute_name: str) -> int:
    return attributes_dict.get(attribute_name)


def get_data() -> pd.DataFrame:
    '''
    Reads data from database if it finds a connection string URI as environmental variable. Otherwise reads data from
    data directory called 'df_input.pkl'.
    :return: pd.DataFrame
    '''
    uri = os.environ.get('URI')
    if uri:
        engine = db.create_engine(uri)
        df = pd.read_sql_table(table_name='df_input', con=engine)
        return df
    else:
        df = pd.read_pickle('./data/df_input.pkl')
        return df
