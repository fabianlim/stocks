from django.shortcuts import render
from django.http import HttpResponse

from forms import SearchForm

from models import Ticker

from utils import match_ticker_to_searchstring
from utils import draw_ticker_figure

import os
cur_dir = os.path.basename(os.path.dirname(os.path.realpath(__file__)))

from common.utils import figure_write_http_response

# Create your views here.


def ticker_png(request):
    """ view to draw the figure image """

    # get the query
    symbol = request.GET.get("symbol")

    # get the ticker figure
    fig = draw_ticker_figure(symbol)

    return figure_write_http_response(fig)


def index(request):
    """ index view with the query searchbar """
    # TODO : this view needs to be changed

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
    return render(request, cur_dir + '/index.html', context)


from models import Quote

from common.utils import df_make_numerical
from common.utils import df_rename_to_verbose_names

import pandas as pd

from datetime import timedelta
from django.utils import timezone


def data_quote(request):
    """ view to deliver data in a json format
        the single parameter allows to specify the
        number of recent days the data is required for """

    days = request.GET.get("days")

    q = Quote.objects.filter(
        date__gte=timezone.now().date()-timedelta(int(days)))

    # get the dataframe from Django model
    df = pd.DataFrame.from_records(q.values())

    # filt_func uses "name", because the df comes from
    # Django model, which uses "name" as field names
    df_make_numerical(df,
                      Quote,
                      df_fields=lambda x: x.name,
                      filt_func=lambda x: x.name)

    # rename to verbose names
    df = df_rename_to_verbose_names(df, Quote)

    # the other way is pd.io.json.read_json
    return HttpResponse(df.to_json(), content_type='application/json')
