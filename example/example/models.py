from django.db import models
from dynamic_forms.models import FormField, ResponseField


class Survey(models.Model):
    topic = models.CharField(max_length=100)

    form = FormField()

    def __str__(self):
        return "Survey #{}: ".format(self.pk, self.topic)


class SurveyResponse(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    response = ResponseField()
