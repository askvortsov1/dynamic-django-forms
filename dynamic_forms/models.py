import json

from django.db import models
from .formfields import FormBuilderField, FormRenderField


class FormField(models.TextField):
    """Stores JSON Schema for form
    """

    def from_db_value(self, value, expression, connection):
        if value is None:
            return []
        return json.loads(value)

    def to_python(self, value):
        if isinstance(value, list):
            return value
        return json.loads(value)

    def get_prep_value(self, value):
        if isinstance(value, str) or value is None:
            return value
        return json.dumps(value)

    def formfield(self, **kwargs):
        kwargs['form_class'] = FormBuilderField
        return super().formfield(**kwargs)


class ResponseField(models.TextField):
    """Stores JSON response to form.
    """

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return json.loads(value)

    def to_python(self, value):
        if isinstance(value, dict):
            return value
        if value is None:
            return {}
        return json.loads(value)

    def get_prep_value(self, value):
        if isinstance(value, str) or value is None:
            return value
        # Datetime.date is not JSON serializable, so must specify to convert to string
        return json.dumps(value, default=str)

    def formfield(self, *args, **kwargs):
        kwargs['form_class'] = FormRenderField
        return super().formfield(*args, **kwargs)
