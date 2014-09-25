# a scratch pad
# getting used to pandas
# and try to get a feel for the data

import pylab as plt
import numpy as np
# from mpl_toolkits.mplot3d import Axes3D


# plot histograms for comparison
def histograms_compare(df, field='pe_ratio'):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    z = 1
    for g in sorted([(a[1].mean(), a[0]) for a in df[field].groupby(level=0)]):
        name = g[1]
        grp = df[field].loc[name]
        vals = grp[grp.notnull()].values
        if len(vals) > 0:
            hist, bins = np.histogram(vals)
            ax.bar(bins[:-1], hist/float(np.sum(hist)),
                   zs=z, zdir='y', alpha=0.8)
            z += 1

    ax.set_xlabel(field)
    ax.set_ylabel('stocks')
    ax.set_zlabel('density')
    ax.set_title(field)
    return (fig, ax)

if __name__ == '__main__':

    # test stuff
    from csv_data.clean_data import unpickle

    df = unpickle()
    histograms_compare('volume')
    plt.show()
