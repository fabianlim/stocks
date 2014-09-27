""" Collection of scripts/utilities """

import urlparse
import json


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

def decode_parameter_uri(params_uri):
    """ decode the param uri into a json dictionary """

    # will return a sequence
    # {param_key : [ list ]}
    keys, vals = zip(*urlparse.parse_qsl(params_uri))

    # use json to parse
    return zip(keys, [json.loads(v.replace('\'', '\"')) for v in vals])
