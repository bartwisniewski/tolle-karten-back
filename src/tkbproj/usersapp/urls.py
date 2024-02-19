from django.urls import path

from . import views

urlpatterns = [
    path(
        "dj-rest-auth/registration/account-confirm-email/<key>/",
        views.EmailConfirmView.as_view(),
        name="account_confirm_email",
    ),
    path(
        "password-reset-confirm/<uidb36>/<key>/",
        views.PasswordResetView.as_view(),
        name="password_reset_confirm",
    ),
]
