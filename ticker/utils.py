from query import QueryInterface

from models import Quote, Historical

from common.utils import get_field_verbose_names
from common.utils import df_make_numerical

from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter


def get_quote_data(symbol):
    """ method to produce an instantaneous quote data """

    if not isinstance(symbol, list):
        symbol = [symbol]

    q = QueryInterface.query_quote(','.join(get_field_verbose_names(Quote)),
                                   ','.join(symbol))

    if q.count == 0:
        return {}

    return q.results


def draw_ticker_figure(symbol, fig=None):

    # TODO: Figure() in the keyargs makes it give to same Figure somehow
    # messing things up
    if fig is None:
        fig = Figure()

    """ method to produce a data plot for the ticker """
    # TODO: implementing plot using historical data, could be changed later

    # get the historical data (this is what we will show)
    q = QueryInterface.query_historicaldata("Volume,Open,Close,Date",
                                            symbol)

    if q.count == 0:
        return fig

    # convert to pandas and make the df numerical
    df = q.to_pandas()
    df_make_numerical(df, Historical)

    # start plotting
    fig.suptitle("ticker {} historical data".format(symbol))

    # dates
    x = df['Date']

    # add the Open and Close data
    ax = fig.add_subplot(211)
    ax.plot_date(x, df['Open'], 'b-x', label='Open')
    ax.plot_date(x, df['Close'], 'r-x', label='Close')
    ax.set_ylabel('Open/Close Prices')
    ax.legend()

    # add the volume data
    ax = fig.add_subplot(212)
    ax.plot_date(x, df['Volume'], 'b-x')
    ax.set_ylabel('Volume')

    # make the date axis nice
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    ax.set_xlabel('Date')

    return fig


def match_ticker_to_searchstring(searchstr):

    """ return the closest ticker to some search text """

    # for the time being implement it this way
    # return Ticker.objects.get(symbol=searchstr)
    return searchstr
