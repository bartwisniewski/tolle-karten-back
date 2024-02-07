from django.urls import path

from . import views

urlpatterns = [
    path("", views.WordList.as_view()),
    path("set-results/", views.SetResults.as_view()),
    path("student/", views.StudentGetUpdate.as_view()),
]
