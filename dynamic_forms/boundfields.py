from django.conf import settings
from django.forms.boundfield import BoundField
from django.template.loader import render_to_string


class MultiValueBoundField(BoundField):
    def _subfield_as_widget(self, sub_bf):
        if getattr(settings, "USE_CRISPY", False):
            template = "dynamic_forms/widgets/subfield_crispy.html"
        else:
            template = "dynamic_forms/widgets/subfield.html"
        label = sub_bf.label_tag()
        help_text = sub_bf.field.help_text
        if sub_bf.field_type == 'HTMLField':
            label = ''
            help_text = ''

        return render_to_string(
            template,
            context={
                'label': label,
                'field': sub_bf,
                'help_text': help_text
            }
        )

    def as_widget(self, widget=None, attrs=None, only_initial=False):
        subfield_widgets = []
        for i, subfield in enumerate(self.field.fields):
            sub_bf = BoundField(self.form, subfield, "{}_{}".format(self.name, i))
            sub_bf.field_type = subfield.__class__.__name__
            subfield_widgets.append(self._subfield_as_widget(sub_bf))
        return render_to_string(
            "dynamic_forms/widgets/formrender.html",
            context={'subfields': subfield_widgets}
        )
