from django.shortcuts import render
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

# from common.utils import decode_parameter_uri
from common.utils import query_to_dict

from utils import get_apps_from_qdict
# from utils import reverse_lookup_url_tags

# import urllib

import os
cur_dir = os.path.basename(os.path.dirname(os.path.realpath(__file__)))


def dashboard(request):
    """ view to display dashboard """

    # converts QueryDict to dict, QueryDict does not handle nesting
    # well
    qdict = query_to_dict(request.GET)

    context = {"app_sidebar": get_apps_from_qdict(qdict, 'sidebar'),
               "app_main": get_apps_from_qdict(qdict, 'main'),
               "encoded_query_string": request.GET.urlencode()}

    return render(request, cur_dir + '/dashboard.html', context)


def search(request):
    """ view to display search """

    qdict = query_to_dict(request.GET)

    # you might be able to skip this redirect if you used AJAX to
    # update the url of the Go button wheneve the user types something in
    if request.method == "POST":
        # replace the search string with the form query
        searchstr = request.POST["navbar-search-text"].strip()

        # make a copy of the query dict
        qcopy = request.GET.copy()

        # update the search string
        qcopy['search'] = searchstr

        # redirect
        return redirect(reverse('search') + '?' +
                        qcopy.urlencode())

    # add the search string to qdict of each app
    # TODO : this may clash the key used in val
    # to workaround i try to chose a more unique key such as ?keys?
    qdict = [(name, dict(val, **{'?keys?': request.GET["search"]}))
             for name, val in qdict if
             isinstance(val, dict)]

    # TODO: I might need to search within apps that are not currently in use,
    # so may need to populate the context with un-used apps.
    # How to do this?
    context = {"app_sidebar": get_apps_from_qdict(qdict, 'sidebar'),
               "app_search": get_apps_from_qdict(qdict, 'search'),
               "searchstr": request.GET["search"],
               "encoded_query_string": request.GET.urlencode()}

    return render(request, cur_dir + '/dashboard.html', context)
