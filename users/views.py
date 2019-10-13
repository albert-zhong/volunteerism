from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from .forms import MyUserCreationForm


class SignUpView(CreateView):
    form_class = MyUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class PendingInvitationsListView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'pending_invitations.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events_with_pending_invitations'] = self.request.user.pending_invitations.all()
        return context