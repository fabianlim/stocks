#!/usr/bin/env/python
from subprocess import check_output

def run_heroku_sql(cmd):
    return check_output(['heroku',
          'pg:psql',
          'DATABASE_URL',
          '-c',
           cmd])

# this is the datetime
dt = run_heroku_sql('SELECT MIN(date+time),MAX(date+time) FROM ticker_quote CSV')
dt = dt.split("\n")[2].replace(' ', '_')
dt = dt.replace('|', '')

print "exporting csv in csv/ directory"
run_heroku_sql(
      """\copy (SELECT * FROM ticker_ticker, ticker_quote WHERE
      ticker_ticker.id=ticker_quote.ticker_id ORDER BY ticker_ticker.name) TO
      csv/heroku_{}.csv CSV HEADER DELIMITER ','""".format(dt) )

print "deleting quote entries"
run_heroku_sql('DELETE FROM ticker_quote')
run_heroku_sql('DELETE FROM ticker_stockrecord')
