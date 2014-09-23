from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from visual.forms import SearchForm

from visual.data_plots_utils import match_ticker_to_searchstring
from visual.data_plots_utils import get_quote_data
from visual.data_plots_utils import draw_ticker_figure, get_figure_canvas

from ticker.models import Ticker


def index(request):
    """ index view with the query searchbar """

    # A HTTP POST?
    if request.method == 'POST':
        form = SearchForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():

            # Save the search object
            search = form.save(commit=True)

            # search text
            # qtext = form.cleaned_data['query']

            # creates the search
            try:
                symbol = match_ticker_to_searchstring(search.text)

                # Now call the visual view
                # The user will be shown the plot
                return ticker_png(request, symbol)

            except Ticker.DoesNotExist:
                print """
                Search text {}: no matching Ticker found
                """.format(search.text)
        else:
            # The supplied form contained errors
            # Just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = SearchForm()

    context = {'form': form}
    return render(request, 'visual/index.html', context)


def visualize_ticker(request, symbol):
    """ view to display information about the ticker """

    # get ticker
    tick = get_object_or_404(Ticker, symbol=symbol)

    # get quote
    quote = get_quote_data(symbol)

    # context
    context = {'symbol': symbol,
               'tick': tick,
               'quote': quote}
    return render(request, 'visual/ticker.html', context)


def ticker_png(request, symbol):
    """ view to draw the figure image """

    # get the ticker figure
    fig = draw_ticker_figure(symbol)

    # get the figure canvas
    canvas = get_figure_canvas(fig)

    # get a image-type HttpResponse
    response = HttpResponse(content_type='image/png')

    # print the png to response
    canvas.print_png(response)

    # clear the figure
    fig.clear()

    # return ther response
    return response
