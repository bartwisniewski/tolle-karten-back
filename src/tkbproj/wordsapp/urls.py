from django.urls import path

from . import views

urlpatterns = [
    path("", views.WordList.as_view(), name="words-list"),
    path("demo/", views.DemoList.as_view(), name="demo-list"),
    path("results/", views.ResultsList.as_view(), name="results"),
    path("set-results/", views.SetResults.as_view(), name="results-set"),
    path("student/", views.StudentGetUpdate.as_view(), name="student"),
    path(
        "generator-task/<pk>/", views.GeneratorTaskGet.as_view(), name="generator-task"
    ),
    path(
        "user-tasks/",
        views.GeneratorTaskUserList.as_view(),
        name="generator-task-user-list",
    ),
]
