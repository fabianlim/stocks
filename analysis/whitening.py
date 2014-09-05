### do a ZCA to whiten the Dataframe
import numpy as np
import pandas as pd

def align_time_series(s):
    result = pd.Series()
    for n in s.index.levels[0]:
        try:
            if s[n].empty==False:
                result = pd.concat([result, s[n].resample('H')],
                    axis=1)
        except Exception as e:
            print "align_time_series: {} Exception {}".format(n,e)
    return result

# group by each feature
def prepare_numeric_matrix(df):
    df = df.drop(['symbol','industry', 'industry_id'],axis=1)
    result = []
    for n in df.columns:
        result += [align_time_series(df[n]).as_matrix(), ]
        print "preparing {}, shape={}".format(n, result[-1].shape)
    return result

# straightforwardly convert to a numeric matrix, removing NaNs
def get_numeric_matrix(df):
    names = set(df.index.levels[0])
    df = df.drop(['symbol','industry', 'industry_id'],axis=1)
    result = df.as_matrix()
    return result[np.isnan(result).sum(axis=1)==0], df.columns, names

from numpy.linalg import svd
# ZCA
# assume the long dimension of M is axis=0
def ZCA_whitening(M):
    K = np.dot(np.transpose(M), M) / M.shape[0]
    print K.shape
    u,s,v = svd(K) #K is hermitian so this is really eigenvalue decomp
    return np.dot(
            np.dot(
                np.dot(M,
                    np.transpose(v)),
                np.diag(1.0/ (np.sqrt(s) + np.spacing(1)))),
            v), s, v


import pickle
from csv_data.clean_data import unpickle
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="""
        Preprocessing first-step.
        Loads dataframe into matrix.
        Apply PCA whitening on data""")
    parser.add_argument('--prep_matrix',
            help="""unpickles [df_file]
                creates the numeric matrix (strips string columes)
                pickles into specified file
                - numeric matrix
                - column names
                - ticker names""",
            nargs='?',
            # default='csv_data/clean_quote_records.p',
            dest='df_file')
    parser.add_argument('matrix_file',
            nargs='?',
            help="""matrix file to either store numeric matrix
                or to take numeric data from""",
            default='analysis/matrix.p')
    args = parser.parse_args()

    if args.df_file:
        print "unpickling dataframe from {}".format(args.df_file)
        # get dataframe
        df = unpickle(filename=args.df_file)

        # prepare numeric matrices
        #mats = prepare_numeric_matrix(df)
        m, cols, names = get_numeric_matrix(df)
        pfile = open(args.matrix_file, 'wb')
        pickle.dump(cols, pfile)
        pickle.dump(m, pfile)
        pickle.dump(names, pfile)
        pfile.close()
    else:

        print "unpickling numeric matrix from {}".format(args.matrix_file)

        #import pickle
        pfile = open(args.matrix_file, 'rb')
        cols = pickle.load(pfile)
        m = pickle.load(pfile)
        pfile.close()

        # using hourly data to ZCA
        m_white, svals, basis = ZCA_whitening(m[::12])

        # plottage
        from pylab import *

        def stock_labeled_axes(title=None, cols=cols):
            fig = figure(tight_layout=True)
            ax = fig.add_subplot(111,
                    title=title)
            ax.set_xticks(range(len(cols)))
            ax.set_xticklabels(cols,
                    rotation="vertical")
            return ax

        ax = stock_labeled_axes('ZCA Whitened Data')
        ax.plot(np.transpose(m_white[::5]))
        ax.grid()

        ax = stock_labeled_axes('feature means (abs value in log scale)')
        ax.plot(np.abs(np.mean(m, axis=0)),
                label='before whitening')
        ax.plot(np.abs(np.mean(m_white, axis=0)),
                label='after whitening')
        ax.set_yscale('log')
        ax.legend()
        ax.grid()

        ax = figure().add_subplot(111, title='singular values')
        ax.plot(svals, '-x')
        ax.set_yscale('log')
        ax.set_xlabel('eigendirection component index')
        ax.grid()

        fig, axs = subplots(3, 1, sharex=True, sharey=True,
                tight_layout=True)
        #ax = stock_labeled_axes('eigen directions')
        for i, ax in enumerate(axs):
            ax.plot(np.transpose(basis[:,i]),
                    label='eigendirection {}'.format(i))
            ax.grid()

        axs[-1].set_xticks(range(len(cols)))
        axs[-1].set_xticklabels(cols,
                    rotation="vertical")

        show()



