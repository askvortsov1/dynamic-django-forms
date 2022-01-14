from django import forms


class HeadingField(forms.Field):
    def __init__(self, attrs=None, *args, **kwargs):
        self.error_messages = {}
        self.is_hidden = False
        self.label_suffix = None
        self.attrs = {'id': False}
        self.show_hidden_initial = False
        self.localize = False
        self.disabled = False
        pass
