import json

from django import forms
from django.utils.html import format_html
from .forms import HTMLField
from django.conf import settings


class FormBuilderWidget(forms.Textarea):
    template_name = "dynamic_forms/widgets/formbuilder.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['DYNAMIC_FORMS_CUSTOM_JS'] = settings.DYNAMIC_FORMS_CUSTOM_JS
        return context

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

    def value_from_datadict(self, data, files, name):
        return data.get(name)
