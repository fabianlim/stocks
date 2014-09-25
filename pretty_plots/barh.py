# very nice plotting by Chris Beaumont from his gitbub ipython notebook
# http://nbviewer.ipython.org/github/cs109/content/blob/master/
#   lec_03_statistical_graphs.ipynb

# from urllib import urlopen

import brewer2mpl
# import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Set up some better defaults for matplotlib
def setup_matplotlib():
    """ setup matlab to look pretty """
    from matplotlib import rcParams

    # colorbrewer2 Dark2 qualitative color table
    dark2_colors = brewer2mpl.get_map('Dark2', 'Qualitative', 7).mpl_colors

    rcParams['figure.figsize'] = (10, 6)
    rcParams['figure.dpi'] = 150
    rcParams['axes.color_cycle'] = dark2_colors
    rcParams['lines.linewidth'] = 2
    rcParams['axes.facecolor'] = 'white'
    rcParams['font.size'] = 14
    rcParams['patch.edgecolor'] = 'white'
    rcParams['patch.facecolor'] = dark2_colors[0]
    rcParams['font.family'] = 'StixGeneral'


def remove_border(axes=None, top=False, right=False, left=True, bottom=True):
    """
    Minimize chartjunk by stripping out unncessary
    plot borders and axis ticks
    The top/right/left/bottom keywords toggle
    whether the corresponding plot border is drawn
    """
    ax = axes or plt.gca()
    ax.spines['top'].set_visible(top)
    ax.spines['right'].set_visible(right)
    ax.spines['left'].set_visible(left)
    ax.spines['bottom'].set_visible(bottom)

    # turn off all ticks
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticks_position('none')

    # now re-enable visibles
    if top:
        ax.xaxis.tick_top()
    if bottom:
        ax.xaxis.tick_bottom()
    if left:
        ax.yaxis.tick_left()
    if right:
        ax.yaxis.tick_right()


def barh(data, tick_labels=None, **kwargs):
    # plt.figure(figsize=(3, 8))
    plt.figure(**kwargs)

    pos = np.arange(len(data))

    # if title:
    #    plt.title(title)
    plt.barh(pos, data)

    # add the numbers to the side of each bar
    for p, d in zip(pos, data):
        plt.annotate(str(d), xy=(d * 1.5, p + .5), va='center')

    # cutomize ticks
    if tick_labels is None:
        ticks = plt.yticks(pos + .5, tick_labels)

    # get rid of xticks
    # xt = plt.xticks()[0]
    # plt.xticks(xt, [' '] * len(xt))

    # minimize chartjunk
    # setup_matplotlib()
    remove_border(left=False, bottom=False)
    plt.grid(axis='x', color='white', linestyle='-')

    # set plot limits
    plt.ylim(pos.max() + 1, pos.min() - 1)
    plt.xlim(0, data.max() * 1.35)

if __name__ == '__main__':

    # simple test
    # data = np.arange(0.1, 0.5, 0.1)
    # labels = ['one', 'two', 'three', 'four']
    # barh(data, tick_labels=labels, title='test')
    # plt.show()

    import pickle
    # plot clustering results
    #  get tick_labels
    filep = open('analytics/matrix.p', 'rb')
    for i in np.arange(0, 3):
        names = pickle.load(filep)  # its the third item
    filep.close()

    # get kmean_labels
    km_labels = pickle.load(open('pretty_plots/clustering/debug.p', 'rb'))

    import pandas as pd
    # get the counts
    d = pd.Series(km_labels, index=names).groupby(level=0).value_counts()
    d = d.reset_index().pivot(index='name', columns='level_1', values=0)
    d[d.isnull()] = 0

    names = d.index.tolist()  # just in case pandas changed my index
    d = d.as_matrix()
    d = d / d.sum(axis=1)[:, np.newaxis]  # normalize

    setup_matplotlib()
    for c in np.arange(0, d.shape[1]):
        d_sort, names_sort = zip(*sorted(zip(d[:, c], names),
                                         reverse=True))
        barh(np.array(d_sort[:10]), tick_labels=names_sort, tight_layout=True)
        plt.show()
