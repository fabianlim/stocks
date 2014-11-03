import numpy as np
from numpy.linalg import svd

import pandas as pd


def pca_compute(df):
    """ compute the princicpal directions and
        return the data in a dataframe"""

    # assume df is numeric
    # get the matrix
    M = df.as_matrix()

    # compute the svd
    K = np.dot(np.transpose(M), M) / M.shape[0]
    u, s, v = svd(K)  # K is hermitian so this is really eigenvalue decomp

    return pd.DataFrame(v, columns=df.columns), s


def zca_whitening(data_df,
                  eigen_df,
                  s):
    """ normalize the data using the eigen dirs and energies """

    # check columns are a match
    # TODO : actually need to check much more
    if data_df.columns != eigen_df.columns:
        return

    # get matrices
    M = data_df.as_matrix()
    v = eigen_df.as_matrix()

    # return the whitened data
    return pd.DataFrame(np.dot(
        np.dot(np.dot(M, np.transpose(v)),
               np.diag(1.0 / (np.sqrt(s) + np.spacing(1)))), v),
        columns=data_df.columns)

from matplotlib.figure import Figure
from common.plots import axes_column_labeled


def draw_pca_figure(d,
                    figure='eigen_dirs',
                    fig=None):
    """ method to produce a data plot for the pca """

    # TODO: Figure() in the keyargs makes it give to same Figure somehow
    # messing things up
    if fig is None:
        fig = Figure(tight_layout=True)

    if figure == 'eigen_dirs' or figure is None:

        eigen_dirs = pd.io.json.read_json(
            d.json_data["eigen_dirs"])

        M = eigen_dirs.as_matrix()
        for i in xrange(3):
            # create axis
            ax = fig.add_subplot(310 + i + 1)

            # get axes
            if i is 2:
                ax = axes_column_labeled(ax,
                                         title="eigen directions",
                                         cols=eigen_dirs.columns)

            ax.plot(M[i, :])

    elif figure == 'singular_values':

        # create axis
        ax = fig.add_subplot(111,
                             title='singular values',
                             yscale='log')

        # get axes
        ax.plot(d.json_data["singular_values"])
    else:
        print "invalid figure {}".format(figure)

    return fig
