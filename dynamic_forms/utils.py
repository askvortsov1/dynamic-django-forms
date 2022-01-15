from django import forms
from .forms import HTMLField
from .widgets import HTMLFieldWidget


def _process_checkbox(field_json):
    field = forms.MultipleChoiceField()
    field.widget = forms.CheckboxSelectMultiple()
    return field


def _process_date(field_json):
    field = forms.DateField()
    field.widget.input_type = "date"
    return field


def _process_email(field_json):
    return forms.EmailField()


def _process_hidden(field_json):
    field = forms.CharField()
    field.widget = forms.HiddenInput()


def _process_number(field_json):
    return forms.FloatField(
        min_value=field_json.get("min", None),
        max_value=field_json.get("max", None),
        widget=forms.NumberInput(attrs={'step': field_json.get("step", "any")})
    )


def _process_radio(field_json):
    field = forms.ChoiceField()
    field.widget = forms.RadioSelect()
    return field


def _process_select(field_json):
    if (field_json.get('multiple', False)):
        return forms.MultipleChoiceField()
    return forms.ChoiceField()


def _process_text_input(field_json):
    return forms.CharField(max_length=field_json.get("maxlength", None))


def _process_text_area(field_json):
    field = forms.CharField()
    field.widget = forms.Textarea()
    return field


def _process_url(field_json):
    return forms.URLField()


def _process_heading(field_json):
    field = HTMLField()
    field.widget = HTMLFieldWidget(params=field_json)
    return field


def _process_paragraph(field_json):
    field = HTMLField()
    field.widget = HTMLFieldWidget(params=field_json)
    return field


TYPE_MAPPING = {
    'checkbox-group': _process_checkbox,
    'date': _process_date,
    'email': _process_email,
    'hidden': _process_hidden,
    'number': _process_number,
    'radio-group': _process_radio,
    'select': _process_select,
    'text': _process_text_input,
    'textarea': _process_text_area,
    'header': _process_heading,
    'paragraph': _process_paragraph,
    'url': _process_url
}


def process_field_from_json(field_json):
    if not isinstance(field_json, dict):
        raise TypeError("Each field JSON must be a dictionary")
    field_type = field_json['type']
    common_field_attrs = {
        'required': field_json.get('required', False),
        'label': field_json.get('label', None),
        'initial': field_json.get('value', None),
        'help_text': field_json.get('description', None),
    }

    common_widget_attrs = {
        'required': field_json.get('required', False),
        'placeholder': field_json.get('placeholder', False),
        'class': field_json.get('className', False),
    }
    field = TYPE_MAPPING[field_type](field_json)
    for attr, val in common_field_attrs.items():
        if field_type not in ['paragraph', 'header']:
            setattr(field, attr, val)
    if field_type not in ['radio-group']:
        for attr, val in common_widget_attrs.items():
            field.widget.attrs[attr] = val
    if field_type in ['checkbox-group', 'radio-group', 'select']:
        choices = [
            (choice['value'], choice['label']) for choice in field_json['values']
        ]
        field.choices = choices
        field.widget.choices = choices
    return field


def gen_fields_from_json(form_json):
    if not isinstance(form_json, list):
        raise TypeError("Form JSON must be a list.")
    fields = []
    for field_json in form_json:
        fields.append(process_field_from_json(field_json))
    return fields
