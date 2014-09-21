#!/usr/bin/env/python
from subprocess import check_output, Popen, PIPE
import re


def is_heroku_db_full(row_large_size=8000):
    """ check is heroku db full or not """

    # call heroku:info
    print "calling heroku:info"
    ps = Popen(('heroku', 'pg:info'), stdout=PIPE)
    info = check_output(('grep', 'Rows'), stdin=ps.stdout)
    ps.wait()

    # returns info like this
    # info = """Rows:        691/10000 (In compliance)
    #           Rows:        0/10000 (In compliance)"""
    print info

    info = info.split("\n")[0]  # take the  first row

    # search the first number
    num_rows_now = int(re.search('(\d+)',
                                 info).groups()[0])

    # if database is pretty full ...
    if num_rows_now > row_large_size:
        return True
    else:
        print "Rows: {}, still well within large_size {}".format(num_rows_now,
                                                                 row_large_size)
        return False


def run_heroku_sql(cmd):
    """ run sql command on heroku """

    return check_output(['heroku',
                         'pg:psql',
                         'DATABASE_URL',
                         '-c',
                         cmd])

# main code here
if is_heroku_db_full():

    # I should put this somewhere in settings
    csv_dir = 'csv_data'

    # query the min and max datetime
    dt = run_heroku_sql(
        'SELECT MIN(date+time),MAX(date+time) FROM ticker_quote CSV')
    # format the datetimes
    dt = dt.split("\n")[2].replace(' ', '_')
    dt = dt.replace('|', '')

    # writing the data entries to csv file
    print "exporting csv in {}/ directory".format(csv_dir)
    run_heroku_sql(
        """\copy (SELECT * FROM ticker_ticker, ticker_quote WHERE
        ticker_ticker.id=ticker_quote.ticker_id ORDER BY ticker_ticker.name) TO
        {}/heroku_{}.csv CSV HEADER DELIMITER ','""".format(csv_dir, dt))

    # clearing the database to free space
    print "deleting quote entries"
    run_heroku_sql('DELETE FROM ticker_quote')
    run_heroku_sql('DELETE FROM ticker_stockrecord')
