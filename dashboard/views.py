from django.shortcuts import render

from utils import decode_parameter_uri


import os
cur_dir = os.path.basename(os.path.dirname(os.path.realpath(__file__)))


import importlib


def get_apps_from_params(params, group_name='sidebar'):
    """ helper function to get apps from params """

    apps = []
    for appname, appval in params:
        try:
            # each app must have a DashboardRegistration object defined in the
            # __init__.py
            m = importlib.import_module(appname)

            # get the method for the group we want and put it in f
            f = getattr(m.DashboardRegistration, 'get_app_' + group_name)

            # run f to process appval and append the result to apps
            apps.append(f(appval))
        except ImportError as e:
            print "dashboard-{} ({}): Import error {}".format(group_name,
                                                              appname,
                                                              e)
            pass

    return apps


def dashboard(request, params):
    """ view to display dashboard """

    # decode the params uri into a dictionary
    params = decode_parameter_uri(params)

    context = {"app_sidebar": get_apps_from_params(params, 'sidebar'),
               "app_main": get_apps_from_params(params, 'main')}

    return render(request, cur_dir + '/dashboard.html', context)


def search(request, params, searchstr):
    """ view to display search """

    # decode the params uri into a dictionary
    params = decode_parameter_uri(params)

    # add the search string to params of each app
    # TODO : this may clash the key used in val
    # to workaround i try to chose a more unique key such as ?str?
    params = [(name, dict(val, **{'?str?': searchstr}))
              for name, val in params]

    # TODO: I might need to search within apps that are not currently in use,
    # so may need to populate the context with un-used apps.
    # How to do this?
    context = {"app_sidebar": get_apps_from_params(params, 'sidebar'),
               "app_search": get_apps_from_params(params, 'search')}

    return render(request, cur_dir + '/dashboard.html', context)
