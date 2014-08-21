import argparse

# yql is not supported anymore, but its beautifully written
from yql import *

def run_public_datatables_query(query):
    y = Public()

    # yahoo.finance stocks are in datatables.org
    results = y.execute(query, env='store://datatables.org/alltableswithkeys')

    return results

if __name__ == '__main__':

    query = """SELECT * FROM yahoo.finance.quote
            WHERE symbol in ("GOOG", "MSFT")
            """
    results = run_public_datatables_query(query)
    print results.rows
