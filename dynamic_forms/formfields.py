from django import forms
from .boundfields import MultiValueBoundField
from .widgets import FormBuilderWidget, FormRenderWidget
from .utils import gen_fields_from_json


class FormBuilderField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = FormBuilderWidget
        return super().__init__(*args, **kwargs)


class FormRenderField(forms.MultiValueField):
    def __init__(self, form_json=[], required=False, **kwargs):
        kwargs['error_messages'] = {
            'incomplete': 'Please fill in all required fields.',
        }
        kwargs['fields'] = gen_fields_from_json(form_json)
        kwargs['label'] = ""
        kwargs['require_all_fields'] = False
        kwargs['required'] = required
        del kwargs['max_length']
        super().__init__(**kwargs)
        self.configure_widget()

    def get_bound_field(self, form, field_name):
        return MultiValueBoundField(form, self, field_name)

    def configure_widget(self):
        widgets = [field.widget for field in self.fields]
        self.widget = FormRenderWidget(widgets)

    def _configure_new_fields(self, fields):
        for f in fields:
            f.error_messages.setdefault('incomplete', self.error_messages['incomplete'])
            if self.disabled:
                f.disabled = True
            if self.require_all_fields:
                # Set 'required' to False on the individual fields, because the
                # required validation will be handled by MultiValueField, not
                # by those individual fields.
                f.required = False
        return tuple(fields)

    def add_fields(self, form_json):
        self.fields += self._configure_new_fields(gen_fields_from_json(form_json))
        self.configure_widget()

    def replace_fields(self, form_json):
        self.fields = self._configure_new_fields(gen_fields_from_json(form_json))
        self.configure_widget()

    def compress(self, data):
        result = {}
        for i, val in enumerate(data):
            result[self.fields[i].label] = val
        return result
