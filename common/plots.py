

def axes_column_labeled(ax,
                        title=None,
                        cols=[]):
    """ helper function to
    1) generate a new fig (with a tight layout (with a tight layout)
    2) plot column labeled axes. The labels are displayed nicely """

    # ax = fig.add_subplot(111, title=title)
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels(cols, rotation="vertical")
    return ax
