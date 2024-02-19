from allauth.account.views import ConfirmEmailView, PasswordResetFromKeyView
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


class PasswordResetView(PasswordResetFromKeyView):
    pass
    # template_name = "usersapp/password-reset.html"
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["uid"] = self.kwargs["uid"]
    #     context["token"] = self.kwargs["token"]
    #     return context
    #
    # # def post(self, request, *args, **kwargs):
    # #     confirmation = self.get_object()
    # #     confirmation.confirm(self.request)
    # #     return HttpResponseRedirect("/")
