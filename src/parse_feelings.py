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
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

assert len(sys.argv) == 2, "You must provide a single positional argument"

# DB connection
conn = utils.get_conn()

# get raw data
print("Loading raw data ...")
dat = utils.get_data(conn)

# subset data to the following columns
keep_col = ['created_utc','downs','edited','gilded','id','is_self','name',
            'num_comments','over_18','score','selftext','subreddit',
            'subreddit_id','title','ups']
    
# clean-up submission title
print("Extracting feelings from raw data ...")
col = 'feeling'
dat[col] = dat.apply(utils.extract_feeling, axis=1)
keep_col.append(col)

# parse sentiments with vaderSentiment
print("Parsing vaderSentiments ...")
sa = SentimentIntensityAnalyzer()
vs = dat.feeling.map(lambda i: sa.polarity_scores("I feel " + i))
dat = dat.join(pd.DataFrame(index=vs.index, data=vs.values.tolist()))
keep_col += ['neg','neu','pos','compound']

# parse sentiment with TextBlob
print("Parsing TextBlob sentiments ...")
tb = dat.feeling.map(lambda i: TextBlob("I feel " + i).sentiment)
dat = dat.join(pd.DataFrame(index=tb.index, data=tb.values.tolist()))
keep_col += ['polarity','subjectivity']

# write to database
dat[keep_col].to_sql(sys.argv[1], conn, if_exists='replace')
print("Results written to table " + sys.argv[1])
