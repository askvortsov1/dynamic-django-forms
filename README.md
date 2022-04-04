# Dynamic Django Forms

**dynamic-django-forms** is a simple, reusable app that allows you to build (and respond to) dynamic forms, i.e. forms that have variable numbers and types of fields. A few examples of uses include:

1. Building and sending out surveys
2. Job applications where each job might have a different application forms

## Installation

Install via pip:

`pip install dynamic-django-forms`

Add to settings.INSTALLED_APPS:

``` python
INSTALLED_APPS = {
    "...",
    "dynamic_forms",
    "..."
}
```

## Components

The main functionality of `dynamic-django-forms` is contained within 2 model fields:

### Form Builder

`dynamic_forms.models.FormField` allows you to build and edit forms via a convenient UI, and stores them in JSON-Schema form. It is easy to use both through the admin panel and in any custom template webpage.

Example Setup:

``` python
from dynamic_forms.models import FormField

class Survey:
    # Other Fields Here
    form = FormField()
```

Please note that JSON data can saved into the model field as a python `dict` or a valid JSON string. When the value is retrieved from the database, it will be provided as a `list` containing `dict`s for each dynamic form field.

### Form Response

`dynamic_forms.models.ResponseField` allows you to render, and collect responses to, forms built with the Form Builder. It is currently only supported through custom views. All form responses are stored as a dict where the key is the question label, and the value is the user's input.

Example Setup:

Model Config:
``` python
from django.db import models
from dynamic_forms.models import ResponseField
from otherapp.models import Survey

class SurveyResponse:
    # Other Fields Here
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE) # Optional
    response = ResponseField()
```

Please note that including a ForeignKey link from the model containing responses to the model containing forms isnt technically required; however, it is highly recommended and will make linking the two much easier

### Configuring ResponseFields with forms

You must provide a valid JSON Schema to ResponseField's associated FormField at runtime. This is best done in the view where the dynamic form will be used. Generally speaking, this means you should:
1. Obtain the JSON Schema Form Data
   * Get an instance of a model containing a FormField that has already been built OR
   * Provide the form data as a constant
2. Intercept the Form instance used in the view where the dynamic form will be shown. This could be an automatically generated ModelForm (via a generic Class Based View), or a form instance you have made yourself.
3. Provide the JSON form data to the form field:
   * form_instance.fields['response_field_name_in_form'].add_fields(JSON_DATA) will add the fields in JSON_DATA to the existing fields in the dynamic form.
   * form_instance.fields['response_field_name_in_form].replace_fields(JSON_DATA) will remove any fields currently in the dynamic form and replace the with the fields in JSON_DATA

An example of how to do this can be found in the DynamicFormMixin explained in the next section:

``` python
from django.views.generic.edit import FormMixin

class DynamicFormMixin(FormMixin):
    form_field = "form"
    form_pk_url_kwarg = "pk"

    response_form_fk_field = None
    response_field = "response"

    def _get_object_containing_form(self, pk):
        return self.form_model.objects.get(pk=pk)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        # Get instance of model containing form used for this response. Save this object as an instance variable for use in form_valid method
        form_instance_pk = self.kwargs[self.form_pk_url_kwarg]
        self.form_instance = self._get_object_containing_form(form_instance_pk)
        # Get json form configuration from form-containing object
        json_data = getattr(self.form_instance, self.form_field)
        # Add fields in JSON to dynamic form rendering field.
        form.fields[self.response_field].add_fields(json_data)
        return form

    def form_valid(self, form):
        action = form.save(commit=False)
        action.survey = self.form_instance
        action.save()
        return super().form_valid(form)
```

#### Configuration Shortcut

The process of configuring ResponseFields with forms is somewhat complicated, so a shortcut is provided.

`dynamic_forms.views.DynamicFormMixin` can be added to Class Based Views extending from `django.views.generic.edit.CreateView` and `django.views.generic.edit.UpdateView`, and will automatically complete configure the dynamic form provided that:

1. The model containing the ResponseField has a ForeignKey link to a model containing the FormField.
2. The following attributes are provided:
   1.  `form_model`: The relevant model (not instance) containing a FormField with the wanted dynamic form configuration. I.e. which model is the survey defined in? Default: `None`
   2.  `form_field`: The attribute of `form_model` that contains the FormField. I.e. Which field in the Survey model contains the form? Default: `form`
   3.  `form_pk_url_kwarg` The [URL Keyword Argument](https://docs.djangoproject.com/en/2.2/topics/http/urls/#passing-extra-options-to-view-functions) containing the primary key of the instance of `form_model` that contains the dynamic form we want? I.e. Which survey are we responding to? Default: `pk`
   4.  `response_form_fk_field` The attribute of the model which contains the ResponseField that links via ForeignKey to the model containing the FormField. I.e. Which attribute of the Survey Response model links to the Survey model? Default: `None`
   5.  `response_field` The attribute of the Response model which contains the ResponseField. I.e. which attribute of the Survey Response model contains the actual responses? Default: `response`

Example:

``` python 
class RespondView(DynamicFormMixin, CreateView):
    model = SurveyResponse
    fields = ['response']
    template_name = "example/respond.html"

    form_model = Survey
    form_field = "form"
    form_pk_url_kwarg = "survey_id"
    response_form_fk_field = "survey"
    response_field = "response"

    def get_success_url(self):
        return reverse('survey_detail', kwargs={"survey_id": self.form_instance.pk})
```

### Django Crispy Forms Support

If you are using [Django Crispy Forms](https://github.com/django-crispy-forms/django-crispy-forms) to make your forms look awesome, set use the following setting:

`USE_CRISPY = True` (false by default)

Please note that you are responsible for importing any CSS/JS libraries needed by your chosen crispy template pack into the templates where (e.x. bootstrap, uni-form, foundation).

## Fields Supported and Limitations

`dynamic-django-forms` currently supports the following field types:

* Checkbox Group
* Date Field
* Hidden Input
* Number
* Radio Group
* Select
* Text Field
* Email Field
* Text Area

The only major limitation of `dynamic-django-forms`, which is also one of its major features, is the dissociation of dynamic form questions and responses.

Pros:

* Responses cannot be changed after submission
* Dynamic forms can be edited, removing, changing, or adding questions, without affecting prior responses

Cons:

* Responses cannot be changed after submission

## Custom JS for FormBuilder

On `settings.py` you can use a variable to inject custom JS code before the form builder is initialized. Note that the `options` variable. Note that when this custom JS runs, the following variables are available:

- `textArea`: This is a hidden textarea input used to submit the JSON form schema.
- `options`: This is a [FormBuilder Options object](https://formbuilder.online/docs/) that you can override and modify to change how the form is displayed.

```
DYNAMIC_FORMS_CUSTOM_JS = 'console.log(1)'
```

## Example Site

To run an example site, run `cd example && docker-compose up`. If you do not use docker, you can manually install the requirements with `pip install -r example/requirements.txt` and run the site with `python example/manage.py runserver`.

## Planned Improvements

* Support for some HTML Elements
  * Headers
  * Paragraph Text
  * Dividers
* Support for the following fields:
  * Color Field
  * Telephone Field
  * Star Rating
* Support for "Other" option on radio groups, checkbox groups, and select dropdowns
  * User can select "other", at which point an inline text-type input will appear where they can put a custom choice
* Ability to provide default JSON form config via:
  * String
  * Dict
  * File
  * Remote URL
* DynamicFormMixin should support slugs
* Ability to customize JSONBuilder settings through Django settings
* Extensive Automated Testing

### Possible Improvements

* Support File Upload Field

## Credits

Huge thanks to Kevin Chappell & Team for developing the awesome open source [Form Builder UI](https://github.com/kevinchappell/formBuilder)!
