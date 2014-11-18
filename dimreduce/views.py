# Create your views here.

# from common.utils import decode_parameter_uri
from common.utils import get_df_from_json_response

from models import Data
import json

from utils import pca_compute
from utils import draw_pca_figure

from common.utils import figure_write_http_response
# from common.utils import query_to_dict
from django.core.cache import cache


def pca(request,
        procedure_name="pca"):
    """
        view to process data and produce the dimension reduction
        requires QueryDict to have the following keys
        figure:
        input:
    """
    # QueryDict doesnt handle nested dicts
    # very well, so this is our fix..
    # qdict = dict(**query_to_dict(request.GET))
    # TODO: assume QueryDict is single level
    # try to just use the plain QueryDict
    # qdict = query_to_dict(request.GET)
    qdict = request.GET

    # if already done, get the response
    d = Data.objects.filter(
        procedure=procedure_name,
        parameters=json.dumps(qdict['input']))
    if d:
        d = d.order_by('input_validity')[0]

    TIME_OUT = 60 * 5
    if not d and cache.add(procedure_name, 'true', TIME_OUT):
        print "acquired cache"
        try:

            # get the df from the input view
            df = get_df_from_json_response(request,
                                           qdict['input'])

            # get the zca results
            # TODO : not sure if this is right way to handle
            # missing data and also to get numeric data
            eigen_dirs, singular_values = pca_compute(
                df.fillna(0)._get_numeric_data())

            d = Data.objects.create(
                procedure=procedure_name,
                parameters=json.dumps(qdict['input']),
                text_desc=("ZCA whitening dimension" +
                           " reduction linear"),
                json_data=json.dumps(
                    {"eigen_dirs": eigen_dirs.to_json(),
                     "singular_values":
                     singular_values.tolist()}),)
        finally:
            print "released cache"
            cache.delete(procedure_name)

    # get figure
    if d:
        return figure_write_http_response(
            draw_pca_figure(d,
                            figure=qdict['figure']))
    else:
        return figure_write_http_response()
