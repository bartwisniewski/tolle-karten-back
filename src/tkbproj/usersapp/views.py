from allauth.account.views import ConfirmEmailView
from django.http import HttpResponseRedirect


class EmailConfirmView(ConfirmEmailView):
    template_name = "usersapp/email-confirm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["key"] = self.kwargs["key"]
        return context

    def post(self, request, *args, **kwargs):
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return HttpResponseRedirect("/")
