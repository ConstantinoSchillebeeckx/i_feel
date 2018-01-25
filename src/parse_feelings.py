#!/usr/bin/env python

'''
description:

    Parse the raw, scraped reddit data by converting the submission titles
    into "feelings" and output the results into a new database table defined
    by the first positional argument.

usage:

    python parse_feelings.py parsed_feelings
'''


import pandas as pd
import utils, sys

assert len(sys.argv) == 2, "You must provide a single positional argument"

conn = get_conn()

# get raw data
print("Loading raw data ...")
dat = utils.get_data(conn)
    
# extract feelings
print("Extracting feelings from raw data ...")
dat['feeling'] = dat.apply(utils.extract_feeling, axis=1)

# subset data to the following columns
keep_col = ['created_utc','downs','edited','gilded','id','is_self','name',
            'num_comments','over_18','score','selftext','subreddit',
            'subreddit_id','title','ups','feeling']

# write to new database table
dat[keep_col].to_sql(sys.argv[1], conn, if_exists='replace')
print("Results written to table " + sys.argv[1])
