from django.urls import reverse
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from dynamic_forms.views import DynamicFormMixin
from .models import Survey, SurveyResponse


class IndexView(TemplateView):
    template_name = "example/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['surveys'] = Survey.objects.all()
        return context


class BuildView(CreateView):
    model = Survey
    fields = '__all__'
    template_name = "example/build.html"
    success_url = "/"


class SurveyDetailView(DetailView):
    model = Survey
    pk_url_kwarg = "survey_id"
    template_name = "example/survey_detail.html"


class SurveyEditView(UpdateView):
    model = Survey
    fields = '__all__'
    pk_url_kwarg = "survey_id"
    template_name = "example/survey_edit.html"

    def get_success_url(self):
        return reverse('survey_detail', kwargs={"survey_id": self.object.pk})


class RespondView(DynamicFormMixin, CreateView):
    model = SurveyResponse
    fields = ['response']
    template_name = "example/respond.html"

    form_model = Survey
    form_pk_url_kwarg = "survey_id"
    response_form_fk_field = "survey"
    response_field = "response"

    def get_success_url(self):
        return reverse('survey_detail', kwargs={"survey_id": self.form_instance.pk})

