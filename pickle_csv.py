# aggregate data from the csv file and pickle

import pandas as pd

# returns a list of csv files in specified mypath
# directory
# filenames are returned with mypath
# prepended in front
# list comprehension, may be slow if there are
# may files
from os import listdir
from os.path import isfile, join
def list_csv_files(mypath):
    return [ mypath + '/' + f for f in listdir(mypath) if isfile(join(mypath,f)) and
            f.endswith(".csv")]

# opens the file 'filename' and reads it with
# pandas' csv reader
def open_and_read_csv(filename):
    with open(filename, 'r') as csvfile:
       return pd.io.parsers.read_csv(filename)

# searches for csv files in 'mypath' directory
# opens them...
# and concatenates all into one pandas DataFrame
# duplicates are not managed
def get_all_csv_records(mypath):
    mats = ()
    for f in list_csv_files(mypath):
        print f
        mats += (open_and_read_csv(f),)
        mats = (pd.concat(mats,axis=0),)
    if mats is ():
        return pd.DataFrame()
    else:
        return mats[0]

import pickle
# pickles the records into a file
def pickle_records(pickle_file, csv_dir='csv_data'):
    records = get_all_csv_records(csv_dir)
    pickle.dump(records, open(csv_dir + '/' + pickle_file, 'wb'))
    print "pickled pandas Dataframe of {} records into file {}".format(
            len(records),
            pickle_file)

# execute stuff
pickle_records('quote_records.p')
