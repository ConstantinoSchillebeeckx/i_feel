#!/usr/bin/env python

'''
description:

    Scrape data from http://redditlist.com/ in order to categorize
    subreddits into larger categories

usage:

    python scrape_reddit_categories.py
'''

import pandas as pd
import urllib2, utils
from bs4 import BeautifulSoup


def get_soup(url):
    page = urllib2.urlopen(url)
    return BeautifulSoup(page, 'html.parser')


categories = {'sfw':{},'nsfw':{}}

# get the main categories for 'sfw' & 'nsfw'
soup = get_soup('http://redditlist.com')
for ul in soup.findAll('ul', attrs={'class':'nested-dropdown'}):
    for li in ul.contents:
        category = li.string.strip().lower().strip()
        group = 'nsfw' if 'nsfw' in unicode(li) else 'sfw'
        if len(li.string.strip()):
            categories[group][category] = []


# find subreddits for each main category
for i in categories.keys():
    for j in categories[i].keys():
        
        url = "http://redditlist.com/%s/category/%s" %(i,j.replace(' ','_'))
        print "Scraping " + url
        dat = get_soup(url)
        
        for k in dat.findAll('div', attrs={'class':'full-page-listing-item'}):
            subreddit = str(k['data-target-subreddit'])

            categories[i][j].append(subreddit)
      

# reformat as df and write to db table `subreddit_categories`
dat = []
table = 'subreddit_categories'
for group in categories.keys():
    for k,v in categories[group].iteritems():
        for i in v:
            dat.append([True if group == 'nsfw' else False, k, i])

dat = pd.DataFrame(dat, columns=['is_nsfw', 'category', 'subreddit'])
dat.to_sql(table, utils.get_conn(), if_exists='replace')
print("reddit categories written to table: " + table)

