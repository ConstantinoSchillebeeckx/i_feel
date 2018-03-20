#!/usr/bin/env python

import re
import pandas as pd
from string import punctuation
from sqlalchemy import create_engine


def get_conn(db_name='i_feel'):
    '''
    Get a sqlalchemy connection engine for the given database
    '''
    return create_engine('postgresql://localhost/'+db_name)

def get_data(conn, table_name = 'raw_query'):
    '''
    Query database for all data in given table. Note that the following
    columns (if present) will be converted to datetime in the returned
    dataframe: ['created_utc','created','approved_at_utc','banned_at_utc']

    Param:
        conn - sqlalchemy engine : database connection
        table_name - str : name of table to query all data for
    
    Return:
        Pandas dataframe
    '''

    df = pd.read_sql('select * from ' + table_name, con=conn, index_col='pk')

    # reformat date columns to human readable
    for col in ['created_utc','created','approved_at_utc','banned_at_utc']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], unit='s')
    
    return df

def extract_feeling(row):
    '''
    Helper function used with .apply() to extract "feeling" from submission title.

    Param:
        row - pandas row object, must have `title` attribute

    Return:
        string of extracted feeling from row.title
    '''
    feeling = re.split(r"(?i)feels?", row.title)[1] # split on feel/feels
    feeling = re.split('[\.!?]', feeling)[0] # remove any trailing sentences
    feeling = re.sub("\[(.*?)\]", "", feeling) # remove flair like '[M29]'
    feeling = feeling.lstrip(punctuation).rstrip('!?.').strip() # removing punctuation

    return feeling

