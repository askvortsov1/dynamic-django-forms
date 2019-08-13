import json

from django import forms


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
