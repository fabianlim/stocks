""" Collection of scripts/utilities for data visualization and
munging """

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

import urlparse
import json


def match_ticker_to_searchstring(searchstr):

    """ return the closest ticker to some search text """

    # for the time being implement it this way
    # return Ticker.objects.get(symbol=searchstr)
    return searchstr


def get_figure_canvas(fig):

    """ method to get the canvas for a plot """

    return FigureCanvas(fig)


def decode_parameter_uri(params_uri):
    """ decode the param uri into a json dictionary """

    # will return a dictionary with first-level keys
    # {key: [ list ]}
    # we assume that each list has only 1 element
    d = urlparse.parse_qs(params_uri)

    for key in d.keys():
        # take the first element
        # replace ' with "
        # and run the json loader
        try:
            d[key] = json.loads(d[key][0].replace('\'', '\"'))
        except ValueError:
            pass  # dont do anything

    return d
