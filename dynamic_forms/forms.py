from django import forms


class HTMLField(forms.Field):
    def __init__(self, attrs=None, *args, **kwargs):
        self.error_messages = {}
        self.label_suffix = None
        self.help_text = None
        self.label = None
        self.initial = ''
        self.required = False
        self.attrs = {'id': False}
        self.show_hidden_initial = False
        self.localize = False
        self.disabled = False
        self.is_hidden = False
