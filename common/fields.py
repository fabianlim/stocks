# custom fields here

from django.db import models

import json
import six


# class JSONField(models.TextField):
class JSONField(six.with_metaclass(models.SubfieldBase,
                                   models.TextField)):

    """ JSON field. Uses Postgres JSON field if available.
    took parts from many online implementations, such as
    http://aychedee.com/2014/03/13/json-field-type-for-django/
    https://github.com/bradjasper/django-jsonfield#other-fields,
    etc ...
    """

    # need this to override to_python
    __metaclass__ = models.SubfieldBase

    def db_type(self, connection):
        if connection.settings_dict[
                'ENGINE'] == 'django.db.backends.postgresql_psycopg2':
            return 'json'
        return 'text'

    def to_python(self, value):
        if value is None:
            return value
        try:
            return json.loads(value)
        except (TypeError, ValueError):
            return value

    def get_prep_value(self, value):
        '''The psycopg adaptor returns Python objects,
        but we also have to handle conversion ourselves
        '''

        try:
            return json.dumps(value)
        except (TypeError, ValueError):
            return value

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([],
                            ["^common\.fields\.JSONField"])
except ImportError:
    pass
