from django.urls import path

from . import views

urlpatterns = [
    path(
        "dj-rest-auth/registration/account-confirm-email/<key>/",
        views.EmailConfirmView.as_view(),
        name="account_confirm_email",
    ),
]
