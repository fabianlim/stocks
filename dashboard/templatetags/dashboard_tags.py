from django import template
from django.core.urlresolvers import reverse

import urllib

from common.utils import query_to_dict

register = template.Library()


def updated_query(request, *args):
    """ takes the query dict in request and
    updates it
    update-in function in clojure sense
    """
    # NOTE: it returns a dict not a QueryDict

    # recall query_to_dict returns key-val sequence
    # filter out the search key
    updated = {k: v for k, v in query_to_dict(request.GET.copy()) if
               k != "search"}

    # the args must at least have a key + value
    if len(args) < 2:
        return updated

    # helper function to update key-in
    def key_in(dic, keys, val):
        k = keys[0]
        # TODO : broken in the sense that I seem to be only updating
        # lists
        if len(keys) == 1:
            if isinstance(dic[k], list) and val not in dic[k]:
                dic[k].append(val)
        else:
            key_in(dic[k], keys[1:], val)

    # call key_in to update
    key_in(updated, args[:-1], args[-1])

    # return the updated dict (NOTE: this is not
    # a query dict
    return updated


@register.simple_tag
def updated_query_str(request, *args):
    """ return encoded query string without
    the 'search' key and update
    according to args"""

    return urllib.urlencode(updated_query(request, *args))


@register.simple_tag
def encoded_query_str(request):
    """ return encoded query string without
    the 'search' key """
    return updated_query_str(request)


@register.simple_tag
def url_python(name):
    """
    reverses in python when template reversal
    is not good enough
    """

    return reverse(name)
