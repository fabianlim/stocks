# script to clean the data before analysis
import pandas as pd
import pickle


def tidy_datetime(date, time):
    """ create a date + time stamp by combining """

    # combine data + time.
    # drop the numbers after the '.' in the time field (if exists)
    comb = date + ":" + time.map(lambda x: x.split('.')[0])
    return pd.to_datetime(comb, format='%Y-%m-%d:%H:%M:%S')


def convert_string_data(s):
    """ function for converting string data to numerics """

    try:
        # convert percent
        return s.map(lambda x: float(x.strip('%')),
                     na_action='ignore')
    except:
        pass

    try:
        # convert thousands, millions, billions..
        def conv(x):
            b = [a for a in [('K', 1e3),
                             ('M', 1e6),
                             ('B', 1e9)] if a[0] in x]
            if len(b) == 0:
                return float(x)  # if fail, guess that it has no modifier
            letter, exp = b[0]
            return float(x.strip(letter)) * exp
        return s.map(conv,
                     na_action='ignore')
    except:
        raise ValueError


def convert_strings_to_numeric(df):
    """ convert the strings to numerics """

    for c in df.columns:
        # first notnull elem
        try:
            s = df[c]
            elem = s[s.notnull()].iloc[0]
            # elem = s.iloc[s.first_valid_index()]
            if isinstance(elem, basestring):
                df[c] = convert_string_data(s)
                print """[OK] column [{}] string type
                      converted sucessfully
                      """.format(c)
        except IndexError:
            print "[ERR] column [{}] all null elems".format(c)
        except ValueError:
            print "[ERR] column [{}] no rule to convert string type".format(c)
    return df


def limit_range(s, min_val, max_val):
    """ function to limit range """

    return s.map(lambda x: max(x, min_val),
                 na_action='ignore').map(lambda x: min(x, max_val),
                                         na_action='ignore')


def drop_stocks_with_low_volume(df):
    """ drop stocks with low volume """

    grp = df.groupby(level=0)
    dropped_stocks = [a for a in df.index.levels[0] if
                      grp['pe_ratio'].count().ix[a] == 0 or
                      grp['volume'].mean().ix[a] < 100000]
    return df.drop(dropped_stocks, level=0)


def unpickle(filename='csv_data/clean_quote_records.p'):
    return pickle.load(open(filename, 'rb'))

if __name__ == '__main__':

    # load the dataframe
    mydir = 'csv_data'
    pickle_file = 'quote_records.p'
    print "loading file {}".format(mydir + '/' + pickle_file)
    df = unpickle(mydir + '/' + pickle_file)

    print "tidying up dateimes"
    # put the tidied datetime in qtime
    df['qtime'] = tidy_datetime(df['date'], df['time'])

    # put tidied last trade time too
    # df['last_trade'] = tidy_datetime(df['last_trade_date'],
    #                                  df['last_trade_time'])

    print "dropping unwanted fields"
    # drop stuff I dont need
    df = df.drop(['date', 'time', 'id',
                  'stockrecord_ptr_id', 'ticker_id',
                  'last_trade_date', 'last_trade_time',
                  'annual_gain', 'last_trade_price'], axis=1)

    print "dropping fields with many NaNs"
    df = df.drop(['dividend_yield', 'oneyr_target_price',
                  'peg_ratio', 'price_eps_est_current_year',
                  'price_eps_est_next_year'], axis=1)

    print "limiting ranges"
    # limit some ranges
    df['price_book'] = limit_range(df['price_book'], -3, 5)

    print "re-indexing"
    # re-index
    df = df.set_index(['name', 'qtime']).sort_index()

    print "dropping unwanted stocks"
    # drop stocks with low volume
    df = drop_stocks_with_low_volume(df)

    print "converting strings to numerics"
    df = convert_strings_to_numeric(df)

    print "pickling"
    # write data to a clean pickle file
    pickle.dump(df, open(mydir + '/clean_' + pickle_file, 'wb'))

    print "cleaned data .."
