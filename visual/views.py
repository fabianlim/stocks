from django.shortcuts import render
from django.http import HttpResponse

from visual.forms import SearchForm

from visual.data_plots_utils import match_ticker_to_searchstring
from visual.data_plots_utils import get_ticker_figure, get_figure_canvas

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
                tick = match_ticker_to_searchstring(search.text)

                # Now call the visual view
                # The user will be shown the plot
                return visualize_ticker(request, tick)

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


def visualize_ticker(request, tick):
    """ view to deliver some visualization of the ticker """

    # query the quote with fields set in the model
    # quote = QueryInterface.query_quote(','.join(Quote.get_fields()),
    #         qtext)

    # if quote.count > 0:
    #     # will create the quote entry in the database, and return
    #     quote_entry = Ticker.query_to_models(qtext, quote.results, Quote)

    #     # get the plot (in string format)
    #     plt_str = tick.plot()

    #     # save will handle duplicate entries
    #     # quote.save()
    #     #context = {'plt_str': plt_str}
    #     #return render(request, 'visual/plot.html', context)

    #     return HttpResponse(plt_str, content_type='image/png')
    # else:
    #     print "did not get any query result with qtext={}".format(qtext)

    # get the ticker figure
    fig = get_ticker_figure(tick)

    # get the figure canvas
    canvas = get_figure_canvas(fig)

    # get a image-type HttpResponse
    response = HttpResponse(content_type='image/png')

    # print the png to response
    canvas.print_png(response)

    # return ther response
    return response
