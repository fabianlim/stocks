""" Collection of scripts/utilities """


# def decode_parameter_uri(params_uri):
#     """ decode the param uri into a json dictionary """
#
#     # will return a dictionary with first-level keys
#     # {key: [ list ]}
#     # we assume that each list has only 1 element
#     d = urlparse.parse_qs(params_uri)
#
#     for key in d.keys():
#         # take the first element
#         # replace ' with "
#         # and run the json loader
#         try:
#             d[key] = json.loads(d[key][0].replace('\'', '\"'))
#         except ValueError:
#             pass  # dont do anything
#
#     return d

import importlib


def get_apps_from_qdict(qdict, group_name='sidebar'):
    """ helper function to get apps from qdict """

    # its essentially a query dict, but is actually in a (key, val) sequence
    # format
    apps = []
    for appname, appval in qdict:
        try:
            # each app must have a DashboardRegistration object defined in the
            # __init__.py
            m = importlib.import_module(appname)

            # get the method for the group we want and put it in get_app_func
            get_app_func = getattr(m.DashboardRegistration,
                                   'get_app_' + group_name)

            # run get_app_func to process appval and append the result to apps
            apps.append(get_app_func(appval))
        except ImportError as e:
            print "dashboard-{} ({}): Import error {}".format(group_name,
                                                              appname,
                                                              e)
            pass

    return apps


# import urllib

# from django.core.urlresolvers import reverse

# def reverse_lookup_url_tags(searchstr):
#     # TODO : is this needed anymore?
#     """ helper function to reverse lookup key url strings """
#     # TODO : it seemed that django template {% url %} tags do not handle
#     # query strings too well, so thats why we do it in python
#
#     # this will return /name/dashboard=?params/
#     # TODO : the reverse lookup does not return absolute paths,
#     # so you need to add '/' in front if you need an absolute path
#     return {'dashboard': urllib.quote(reverse('dashboard',
#                                               args=("p")).strip("p/")),
#             # this will return /name/search=?params/
#             'search': urllib.quote(
#                 reverse('search', args=(searchstr, "p")).strip("p/"))}
