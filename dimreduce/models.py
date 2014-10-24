from django.db import models

# Create your models here.

from common.fields import JSONField

from django.utils import timezone

from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField


class Data(models.Model):
    """ model for processed data """

    """ an aggregated time for when the input data is valid
        Put a timestamp here to let the indicate how fresh
        the input was when the computation was done"""
    input_validity = models.DateTimeField(
        default=timezone.now)

    # official name of process/method/data
    procedure = models.CharField(max_length=20)

    # params
    parameters = models.TextField()

    # basic description of json
    text_desc = models.CharField(max_length=100)

    # json data
    json_data = JSONField()

    # for full-text searching
    search_index = VectorField()

    # search manager for full-text searching
    objects = SearchManager(
        fields=('procedure', 'parameters', 'text_desc'),
        config='pg_catalog.english',
        search_field='search_index',
        auto_update_search_field=True)
