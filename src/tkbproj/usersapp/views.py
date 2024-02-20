from allauth.account.views import (
    ConfirmEmailView,
    PasswordResetFromKeyView,
    PasswordResetView,
)
from django.http import HttpResponseRedirect


class EmailConfirmView(ConfirmEmailView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["key"] = self.kwargs["key"]
        return context

    def post(self, request, *args, **kwargs):
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return HttpResponseRedirect("/")


class ResetPasswordFromKeyView(PasswordResetFromKeyView):
    pass


class ResetPasswordView(PasswordResetView):
    pass
