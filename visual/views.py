from django.shortcuts import render

from forms import SearchForm

from utils import match_ticker_to_searchstring
from utils import decode_parameter_uri

from ticker.models import Ticker  # bad

from ticker.utils import ticker_png  # bad


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

import importlib


def dashboard(request, params):
    """ view to display dashboard """

    # decode the params uri into a dictionary
    params = decode_parameter_uri(params)

    app_sidebar = dict()
    app_main = dict()
    for appname in params.keys():
        try:
            # each app must have a DashboardRegistration object defined in the
            # __init__.py
            m = importlib.import_module(appname)
            app_sidebar[appname] = m.DashboardRegistration.get_app_sidebar(
                params[appname])
            app_main[appname] = m.DashboardRegistration.get_app_main(
                params[appname])
        except ImportError as e:
            print "dashboard ({}): Import error {}".format(appname, e)
            pass

    context = {"app_sidebar": app_sidebar,
               "app_main": app_main}

    return render(request, 'visual/dashboard.html', context)
