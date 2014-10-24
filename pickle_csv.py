import pandas as pd

from os import listdir
from os.path import isfile, join

import pickle

import argparse

""" aggregate data from csv files in the directory, read them into a
    pandas dataframe, and pickle """


def list_csv_files(mypath):
    """ list all the csv files in the mypath directory """

    return [mypath + '/' + f
            for f in listdir(mypath) if isfile(join(mypath, f)) and
            f.endswith(".csv")]


def get_all_csv_records(mypath):
    """ lists csv files in 'mypath' directory
    opens them...
    and concatenates all into one pandas DataFrame
    duplicates are not managed
    """
    mats = ()
    for f in list_csv_files(mypath):
        print f
        mats += (pd.io.parsers.read_csv(f),)
        mats = (pd.concat(mats, axis=0),)
    if mats is ():
        return pd.DataFrame()
    else:
        return mats[0]


def pickle_records(pickle_file, csv_dir='csv_data'):
    """ pickles """

    records = get_all_csv_records(csv_dir)
    pickle.dump(records, open(pickle_file, 'wb'))
    print """pickled pandas Dataframe of {}
            records into file {}""".format(len(records),
                                           pickle_file)


if __name__ == '__main__':

    # execute stuff
    parser = argparse.ArgumentParser(
        description="""pickle csv data into pandas dataframe""")
    parser.add_argument('filename', help='name file to pickle into')
    args = parser.parse_args()

    # call the pickle function
    pickle_records(args.filename)
