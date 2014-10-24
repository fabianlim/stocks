# custom fields here

from django.db import models

import datetime


class FormattedDateField(models.DateField):

    """ Date Field whereby one can specify strptime format """

    # need this to override to_python
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        # store the format
        self._format = kwargs.pop('format', "%Y-%m-%d")
        super(FormattedDateField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return

        # do this conversion if input is string
        if isinstance(value, basestring):
            try:
                value = datetime.datetime.strptime(value, self._format)
            except:
                # if fails the strptime, may be already in default format
                # so just try that
                value = datetime.datetime.strptime(value, "%Y-%m-%d")

        # call the parent's to_python function
        return super(FormattedDateField, self).to_python(value)


class PercentField(models.CharField):

    """ Field with a percentage modifier """

    # need this to override get_prep_value and to_python
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        # CharField need to specify max_length
        kwargs.update(dict(max_length=20))
        super(PercentField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if not value:
            return

        return str(value * 100) + '%'

    def to_python(self, value):
        if not value:
            return

        try:
            return float(value.replace('%', "")) / 100
        except AttributeError:
            # value = nan will give a type error
            return value


class BigFloatField(models.CharField):

    """ Field with thousands, millions, billions ... modifiers """

    # need this to override get_prep_value and to_python
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        # CharField need to specify max_length
        kwargs.update(dict(max_length=20))
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

        try:
            v = [(1e3**(i+1), m) for i, m in
                 enumerate(self._modifiers) if m in value]

            if len(v) == 1:
                e, m = v[0]
                return float(value.replace(m, '')) * e
            else:
                return
        except TypeError:
            # if value is nan will get a type erro
            return value  # return the nan

# for south migrations
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^ticker\.fields\.FormattedDateField"])
    add_introspection_rules([], ["^ticker\.fields\.PercentField"])
    add_introspection_rules([], ["^ticker\.fields\.BigFloatField"])
except ImportError:
    pass
