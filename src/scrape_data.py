#!/usr/bin/env python
"""
description:

    Scrape reddit post titles for the words "I feel" and store results
    into a postgres database. 

    Script assumes that a Postgres database named `i_feel` exsits, and that
    it has a table named `raw_query` (see create_table.sql).

examples:

    python run.py --start 2017-01-01 --end 2018-01-01
"""



import praw, psycopg2, time, argparse
import traceback, os
from psycopg2.extensions import AsIs



class SmartFormatter(argparse.HelpFormatter):
    """
    smart option parser, will extend the help string with the values
    for type e.g. {stype: str} and default (default: None)
    adapted from https://bitbucket.org/ruamel/std.argparse/src/cd5e8c944c5793fa9fa16c3af0080ea31f2c6710/__init__.py?fileviewer=file-view-default
    """

    def __init__(self, *args, **kw):
        self._add_defaults = None
        super(SmartFormatter, self).__init__(*args, **kw)

    def _fill_text(self, text, width, indent):
        return ''.join([indent + line for line in text.splitlines(True)])

    def _split_lines(self, text, width):
        self._add_defaults = True
        text = text
        return argparse.HelpFormatter._split_lines(self, text, width)

    def _get_help_string(self, action):
        help = action.help
        if action.default is not argparse.SUPPRESS:
            defaulting_nargs = [argparse.OPTIONAL, argparse.ZERO_OR_MORE]
            if action.option_strings or action.nargs in defaulting_nargs:
                help += ' {type: %(type)s} (default: %(default)s)'
        return help


def write_listing_to_db(conn, listing, prev_id=set([])):

    # convert/delete some of the listing values
    # so that we can properly insert it into the DB
    dat = {k:v for k,v in vars(listing).items() if type(v) not in [list,dict]}
    dat['subreddit'] = str(dat['subreddit'])
    dat['author'] = str(dat['author'])
    dat['downloaded_utc'] = int(time.time())

    if dat['id'] not in prev_id:

        # prep statement
        # https://stackoverflow.com/a/29471241/1153897
        vals = [v for k,v in dat.items() if k[0] != '_']
        cols = [k for k,v in dat.items() if k[0] != '_']

        sql = 'INSERT INTO raw_query (%s) values %s'
        cursor = conn.cursor()
        statement = cursor.mogrify(sql, (AsIs(','.join(cols)), tuple(vals)))
        cursor.execute(statement)
        conn.commit()


def build_query(kw):

    # Build query with list of keywords
    kw_lower = [l.lower() for l in kw]
    kw_join = '" OR title:"'.join(kw)
    kw_lower_join = '" OR title:"'.join(kw_lower)
    return '(title:"%s" or title:"%s") self:yes' %(kw_join, kw_lower_join) 


def run_query(start, end, debug=False): 

    if debug:
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        logger = logging.getLogger('prawcore')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)


    r = praw.Reddit(client_id='4aMHmE0ESoA2Jg',
                    client_secret='rXseyUpVlrNT6PFkdBt8Uw6hgQE',
                    user_agent='I feel by /u/meowmop',
                    cache_timeout=0)
    r.read_only = True

    eq="(and (or title:'I feel' title:'i feel') is_self:1)"

    return r.subreddit('all').submissions(start, end, extra_query=eq)


def assert_date_format(date, pattern='%Y-%m-%d'):

    '''
    Assert given date string has the pattern YYYY-MM-DD
    '''

    try:
        time.strptime(date, pattern)
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")



def date_to_epoch(date):
    '''
    Convert date (YYY-MM-DD) into epoch time (local timezone)
    '''
    pattern = '%Y-%m-%d'
    return int(time.mktime(time.strptime(date, pattern)))


def get_prev_ids(conn, table_name):
    '''
    Return set of all previously downloaded reddit post IDs.
    '''

    cur = conn.cursor()
    exe = cur.execute("SELECT id FROM public." + table_name)
    return  set([l[0] for l in cur.fetchall()])


# ----------------------------------------------------------------------------#
# --------------------------------- MAIN -------------------------------------#
# ----------------------------------------------------------------------------#
def main (args):

    # error check
    for date in [args.start,args.end]:
        assert_date_format(date)

    # reformat arguments
    start = date_to_epoch(args.start)
    end = date_to_epoch(args.end)
    window = args.window * 86400

    assert end > start, "End date must come after start date."

    # connect to DB, assume local
    db_name = 'i_feel'
    table_name = 'raw_query'
    conn = psycopg2.connect("dbname='%s' host='localhost'" %db_name)

    # lookup previous ids so we don't duplicate data
    prev_id = get_prev_ids(conn, table_name)

    # query reddit
    for day in range(start, end, window):

        print(time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(day)))

        for submission in run_query(day, day+window-1):
            write_listing_to_db(conn, submission, prev_id)


# SETUP OPTION PARSER
if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description=__doc__,
                            formatter_class=SmartFormatter)
        required = parser.add_argument_group('required arguments')
        required.add_argument("-s", "--start", default=None, required=True, 
                              type=str,
                              help="Start date (YYYY-MM-DD) for query.")
        required.add_argument("-e", "--end", default=None, required=True, 
                              type=str,
                              help="End date (YYYY-MM-DD) for query.")
        parser.add_argument("-w", "--window", default=1, required=False, 
                            type=int,
                            help="Query date-range is split into windows of a particular length in days since each query is limited to 1000 results.")
        args = parser.parse_args()
        main(args)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)
