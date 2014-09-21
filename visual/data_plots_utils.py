""" Collection of scripts/utilities for data visualization and
munging """
from ticker.models import Ticker, Historical

# return the closest ticker to some search text
def match_ticker_to_searchstring(searchstr):
    # for the time being implement it this way
    return Ticker.objects.get(symbol=searchstr)

#from matplotlib import pylab
#import PIL
#import PIL.Image
#
#import StringIO
#
#def canvas_to_string(canvas):
#    buffer = StringIO.StringIO()
#    canvas.draw()
#    graphIMG = PIL.Image.frombytes("RGB",
#            canvas.get_width_height(),
#            canvas.tostring_rgb())
#    graphIMG.save(buffer, 'PNG')
#    pylab.close()
#
#    return buffer.getvalue()

from ticker.query import QueryInterface

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# method to get the canvas for a plot
def get_figure_canvas(fig):
    return FigureCanvas(fig)

import datetime
# method to produce a data plot for the ticker
def get_ticker_figure(tick):
    #TODO: implementing plot using historical data, could be changed
    # later
    # get the historical data (this is what we will show)
    #q = QueryInterface.query_historicaldata(','.join(Historical.get_fields()),
    q = QueryInterface.query_historicaldata("Volume,Open,Close,Date",
            tick.symbol)
    import pickle
    pickle.dump(q.results, file('query.p', 'wb'))

    fig = Figure()
    ax = fig.add_subplot(111, title="ticker {} historical data".format(tick.symbol))
    x = [e['Date'] for e in q.results]
    y = [e['Volume'] for e in q.results]
    print x
    print y

    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    ig.autofmt_xdate()
    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')

    return fig
