from django.urls import path

from . import views

urlpatterns = [
    path("", views.WordList.as_view()),
]
