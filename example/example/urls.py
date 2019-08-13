from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name="home"),
    path('survey/new/', views.BuildView.as_view(), name="survey_create"),
    path('survey/<int:survey_id>/', views.SurveyDetailView.as_view(), name="survey_detail"),
    path('survey/<int:survey_id>/edit/', views.SurveyEditView.as_view(), name="survey_edit"),
    path('survey/<int:survey_id>/response/', views.RespondView.as_view(), name="survey_respond"),
    path('survey/<int:survey_id>/response/<int:response_id>/', views.RespondView.as_view(), name="response"),
    path('admin/', admin.site.urls),
]
