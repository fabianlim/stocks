# Create your views here.

# from common.utils import decode_parameter_uri
from common.utils import get_df_from_json_response

from models import Data
import json

from utils import pca_compute
# from utils import draw_pca_figure

# from common.utils import figure_write_http_response
# from common.utils import query_to_dict
from django.core.cache import cache

from django.shortcuts import render

from django.http import HttpResponse

import os
cur_dir = os.path.basename(os.path.dirname(os.path.realpath(__file__)))


def pca_stock_quotes(request):

    d = Data.objects.order_by('input_validity').first()
    input_validity = ''
    if d is not None:
        input_validity = d.input_validity

    return render(request,
                  cur_dir + '/pca-stocks.html',
                  {'input_validity': input_validity})


def pca(request):

    # hate to hardcode paths
    return render(request,
                  cur_dir + '/pca-figure-radial.html')

from django.utils.datastructures import MultiValueDictKeyError
from django.utils import timezone


def data_pca(request,
             procedure_name="pca"):
    """
        view to process data and produce the dimension reduction
        requires QueryDict to have the following keys
        input:
    """

    # if already done, get the response
    d = Data.objects.order_by('input_validity').first()

    if d is None:
        # if d is none, definitely compute
        is_need_compute = True
    else:
        # compute if validity is one day late
        is_need_compute = d.input_validity.date() < timezone.now().date()

    TIME_OUT = 60 * 5
    if is_need_compute and cache.add(procedure_name, 'true', TIME_OUT):
        print "acquired cache"
        try:

            # get the df from the input view
            df = get_df_from_json_response(request,
                                           request.GET['input'])

            # drop columns if specified
            try:
                df.drop(request.GET['drop'], 1, inplace=True)
            except MultiValueDictKeyError:
                # come here if it was a multiValue
                df.drop(request.GET.getlist('drop[]', []), 1, inplace=True)
            except KeyError:
                # come here if the key 'drop' did not exist
                pass

            # get the zca results
            # TODO : not sure if this is right way to handle
            # missing data and also to get numeric data
            eigen_dirs, singular_values = pca_compute(
                df.fillna(0)._get_numeric_data())

            d = Data.objects.create(
                procedure=procedure_name,
                parameters=json.dumps(request.GET['input']),
                text_desc=("ZCA whitening dimension" +
                           " reduction linear"),
                json_data= {"eigen_dirs": eigen_dirs.to_json(),
                            "singular_values":
                                singular_values.tolist()},)
        finally:
            print "released cache"
            cache.delete(procedure_name)

    # return response
    # have to dump json data again because json field deserializes
    return HttpResponse(json.dumps(dict(d.json_data,
                                        input_validity=str(
                                            d.input_validity.strftime('%c')))),
                        content_type='application/json')
