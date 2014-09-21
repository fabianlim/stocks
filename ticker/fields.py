# custom fields here

from django.db import models


class PercentField(models.CharField):

    """ Field with a percentage modifier """

    # need this to override get_prep_value and to_python
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        # CharField need to specify max_length
        kwargs.update(dict(
            max_length=20))
        super(PercentField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if not value:
            return
        return str(value * 100) + '%'

    def to_python(self, value):
        if not value:
            return
        return float(value.replace('%', "")) / 100


class BigFloatField(models.CharField):

    """ Field with thousands, millions, billions ... modifiers """

    # need this to override get_prep_value and to_python
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        # CharField need to specify max_length
        kwargs.update(dict(
            max_length=20))
        super(BigFloatField, self).__init__(*args, **kwargs)

    # TODO can add more modifiers if needed
    _modifiers = ['K', 'M', 'B']

    def get_prep_value(self, value):
        if not value:
            return
        for m in [''] + self._modifiers:
            if value >= 1000.0:
                value /= 1000.0
            else:
                return str(value) + m
        return

    def to_python(self, value):
        if not value:
            return
        v = [(1e3**(i+1), m) for i, m in
             enumerate(self._modifiers) if m in value]

        if len(v) == 1:
            e, m = v[0]
            return float(value.replace(m, '')) * e
        else:
            return
