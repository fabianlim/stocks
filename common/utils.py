import urlparse
import json


def decode_string_to_json(string):
    """ some strings use single quotes which mess up
    json decoders """

    try:
        return json.loads(string.
                          replace('u\'', '\"').
                          replace('\'', '\"'))
    except ValueError:
        return string


from django.http import QueryDict


def query_to_dict(query):
    """ decode the query dict """

    if isinstance(query, basestring):
        return decode_string_to_json(query)
    elif isinstance(query, QueryDict):
        return [(k, decode_string_to_json(v)) for
                k, v in query.dict().items()]
    elif isinstance(query, dict):
        return [(k, decode_string_to_json(v)) for
                k, v in query.items()]
    else:
        raise ValueError("Dont know what to do with {}".format(query))


def decode_parameter_uri(params_uri):
    """ decode the param uri into a json dictionary """

    # will return a sequence
    # {param_key : [ list ]}
    keys, vals = zip(*urlparse.parse_qsl(params_uri))

    try:
        # use json to parse
        return zip(keys, [decode_string_to_json(v) for v in vals])
    except ValueError:
        # if its a single level param dictionary this the json
        # will fail
        return zip(keys, vals)


import urllib2
import pandas as pd


def get_df_from_json_response(request, half_uri):

    # build the full url
    uri = request.build_absolute_uri(half_uri)

    # hack when using Client from django.http.test
    # but server has to be running
    # uri = uri.replace("http://testserver",
    #                   "http://127.0.0.1:8000")

    # open url
    response = urllib2.urlopen(uri)

    # read the html body and return
    return pd.io.json.read_json(response.read())


def get_fields(model, name_filter_list=None,
               attr_func=lambda x: x,
               filt_func=lambda x: x.verbose_name):
    """ helper function to return model fields """

    if name_filter_list is None:
        return [attr_func(f) for f in model._meta.fields]
    else:
        return [attr_func(f) for f in get_fields(model) if
                filt_func(f) in name_filter_list]


def get_field_verbose_names(model,
                            attr_func=lambda x: x.verbose_name,
                            **kwargs):
    """ helper function to return model fields verbose names """

    return get_fields(model,
                      attr_func=attr_func,
                      **kwargs)


def df_make_numerical(df,
                      model,
                      df_fields=lambda x: x.verbose_name,
                      filt_func=lambda x: x.verbose_name):
    """ method to convert columns of df to be numerical """

    for f in get_fields(model,
                        name_filter_list=df.columns,
                        filt_func=filt_func):
        # to_python function is responsible for converting to
        # numerics
        df[df_fields(f)] = df[df_fields(f)].map(lambda x: f.to_python(x))


def df_rename_to_verbose_names(df, model):
    """ rename df columns from terse to verbose names """

    return df.rename(
        columns=dict([(f.name, f.verbose_name) for
                      f in get_fields(model,
                                      name_filter_list=df.columns,
                                      filt_func=lambda x: x.name)]))

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from django.http import HttpResponse


def figure_write_http_response(fig):
    """ helper function to write figure to a
        image type http response """

    # get the figure canvas
    canvas = FigureCanvas(fig)

    # get a image-type HttpResponse
    response = HttpResponse(content_type='image/png')

    # print the png to response
    canvas.print_png(response)

    # clear the figure
    fig.clear()

    # return ther response
    return response


def split_keyval_sequence(kv, it):
    r = []
    for k, v in kv:
        if k is not it:
            r += [(k, v), ]
        else:
            itv = v
    return itv, r


def split_template_from_querydict(qdict):

    return qdict["algo"] + ".html"
