import json

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import smart_unicode
from django.utils.six import with_metaclass


class JSONField(with_metaclass(models.SubfieldBase, models.Field)):

    """Simple JSON field that stores python structures as JSON strings on database.
    """

    def to_python(self, value):
        """
        Convert the input JSON value into python structures, raises
        django.core.exceptions.ValidationError if the data can't be converted.
        """
        if self.blank and not value:
            return None
        if isinstance(value, basestring):
            try:
                return json.loads(value)
            except Exception, e:
                return value
        else:
            return value

    def get_prep_value(self, value):
        """Convert value to JSON string before save"""
        try:
            return json.dumps(value)
        except Exception, e:
            raise ValidationError(str(e))


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^myyum\.rpm\.fields\.JSONField"])
except:
    pass
