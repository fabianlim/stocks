from django.shortcuts import render

from utils import decode_parameter_uri


import os
cur_dir = os.path.basename(os.path.dirname(os.path.realpath(__file__)))


import importlib


def dashboard(request, params):
    """ view to display dashboard """

    # decode the params uri into a dictionary
    params = decode_parameter_uri(params)

    app_sidebar = []
    app_main = []
    for appname, appval in params:
        try:
            # each app must have a DashboardRegistration object defined in the
            # __init__.py
            m = importlib.import_module(appname)
            app_sidebar.append(
                m.DashboardRegistration.get_app_sidebar(appval))
            app_main.append(
                m.DashboardRegistration.get_app_main(appval))
        except ImportError as e:
            print "dashboard ({}): Import error {}".format(appname, e)
            pass

    context = {"app_sidebar": app_sidebar,
               "app_main": app_main}

    return render(request, cur_dir + '/dashboard.html', context)
