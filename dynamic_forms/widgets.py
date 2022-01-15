import json

from django import forms
from django.utils.html import format_html
from .forms import HTMLField


class FormBuilderWidget(forms.Textarea):
    template_name = "dynamic_forms/widgets/formbuilder.html"

    def format_value(self, value):
        if value is None:
            return None
        return json.dumps(value)


class FormRenderWidget(forms.MultiWidget):
    template_name = "dynamic_forms/widgets/formrender.html"

    def decompress(self, value):
        return []


class HTMLFieldWidget(HTMLField):
    def __init__(self, attrs=None, params={}):
        self.attrs = attrs
        self.params = params
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        class_html = ''
        if 'className' in self.params:
            class_html = " class='{0}'".format(self.params['className'])
        return format_html("<{0}{2}>{1}</{0}>".format(self.params['subtype'], self.params['label'], class_html))

    def get(self):
        return False

    def use_required_attribute(self, initial):
        return False

    def id_for_label(self, id):
        return ''

    def get_context(self):
        return {'name': ''}
