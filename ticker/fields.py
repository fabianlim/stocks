### put some custom fields here

from django.db import models

class FloatWithModifierField(models.CharField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.modifier = kwargs.pop('modifier')
        super(FloatWithModifierField, self).__init__(*args, **kwargs)

    def _decons(self, value):
        #assert(value[-1] in self.modifier.keys())
        if value[-1] not in self.modifier.keys():
            raise KeyError
        return float(value[:-1]), value[-1] #may throw ValueError

    def get_prep_value(self, value):
        if not value: return
        if isinstance(value, tuple):
            return value[1]
        return value

    def to_python(self, value):
        if not value: return
        try:
            num_val, unit = self._decons(value.strip())
            return (self.modifier[unit](num_val), value)
        except KeyError:
            return (float(value), value)

class PercentField(FloatWithModifierField):
    def __init__(self, *args, **kwargs):
        kwargs.update( dict(
            max_length=10,
            modifier= {'%': lambda x: x / 100.0 }))
        super(PercentField, self).__init__(*args, **kwargs)

class BigFloatField(FloatWithModifierField):
    def __init__(self, *args, **kwargs):
        kwargs.update( dict(
            max_length=20,
            modifier= {'B': lambda x: x * 1e9,
                       'M': lambda x: x * 1e6,
                       'K': lambda x: x * 1e3}))
        super(BigFloatField, self).__init__(*args, **kwargs)
