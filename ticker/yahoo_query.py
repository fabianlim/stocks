import argparse

# yql is not supported anymore, but its beautifully written
from yql import Public, YQLError

def run_public_datatables_query(query):
    # public query class of yql
    y = Public()

    # yahoo.finance are in datatables.org,
    # so we need this
    results = y.execute(query, env='store://datatables.org/alltableswithkeys')

    return results

if __name__ == '__main__':

    #query = """SELECT * FROM yahoo.finance.quote
    #        WHERE symbol in ("GOOG", "MSFT")
    #        """
    #query = """SELECT * FROM yahoo.finance.stocks
    #        WHERE symbol in ("GOOG", "MSFT")
    #        """
    #query = """SELECT * FROM yahoo.finance.option_contracts
    #        WHERE symbol in ("GOOG", "MSFT")
    #        """
    #query = """SELECT * FROM yahoo.finance.historicaldata
    #        WHERE symbol in ("GOOG", "MSFT")
    #        AND startDate="2009-01-10" AND
    #        endDate="2010-01-01"
    #        """
    #
    parser = argparse.ArgumentParser(description="execute a YQL query")
    parser.add_argument('query', help="""enter the query terms
            enclosed in quotes""")

    args = parser.parse_args()

    try:
        results = run_public_datatables_query(args.query)

        try:
            print "keys: " + " ".join(results.rows[0].keys())
            print "number of rows {}".format(results.count)
            import pylab
            y = [int(r["Volume"]) for r in results.rows]
            pylab.plot(range(len(y)), y)
            pylab.show()
        except IndexError:
            print results.pprint_raw()
    except YQLError as e:
        print e


    # print some stats

    #import pdb
    #pdb.set_trace()
    #print results.rows
