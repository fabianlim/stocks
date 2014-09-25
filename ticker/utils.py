from query import QueryInterface

from models import Quote, Historical
from models import get_fields, get_field_verbose_names

from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from django.http import HttpResponse


def make_numerical_pandas(df, model):

    """ method to convert columns of df to be numerical """

    for f in get_fields(model, name_filter_list=df.columns):
        df[f.verbose_name] = df[f.verbose_name].map(lambda x: f.to_python(x))


def get_quote_data(symbol):
    """ method to produce an instantaneous quote data """

    q = QueryInterface.query_quote(','.join(get_field_verbose_names(Quote)),
                                   symbol)

    if q.count == 0:
        return {}

    return q.results[0]


def draw_ticker_figure(symbol, fig=Figure()):

    """ method to produce a data plot for the ticker """
    # TODO: implementing plot using historical data, could be changed later

    # get the historical data (this is what we will show)
    q = QueryInterface.query_historicaldata("Volume,Open,Close,Date",
                                            symbol)

    if q.count == 0:
        return fig

    # convert to pandas and make the df numerical
    df = q.to_pandas()
    make_numerical_pandas(df, Historical)

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


def ticker_png(request, symbol):
    """ view to draw the figure image """

    # get the ticker figure
    fig = draw_ticker_figure(symbol)

    # get the figure canvas
    canvas = FigureCanvas(fig)

    # get a image-type HttpResponse
    response = HttpResponse(content_type='image/png')

    # print the png to response
    canvas.print_png(response)

    # clear the figure
    fig.clear()

    # return ther response
    return response
