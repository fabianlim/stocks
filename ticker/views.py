from django.shortcuts import render

from forms import SearchForm

from models import Ticker

from utils import ticker_png
from utils import match_ticker_to_searchstring

import os
cur_dir = os.path.basename(os.path.dirname(os.path.realpath(__file__)))

# Create your views here.


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
