from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, DeleteView, CreateView, UpdateView

from .forms import EventEmptyForm, EventCreationForm, EventAddVolunteersForm
from .models import Event

import re


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    fields = (
        'name',
        'description',
        'contact',
        'location',
        'spots',
        'is_public',
        'time',
    )
    template_name = 'events_new.html'
    success_url = reverse_lazy('home')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        return super().form_valid(form)


class EventJoinView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    login_url = 'login'
    success_url = reverse_lazy('event_detail', kwargs={'pk': 1})
    template_name = 'events_join.html'
    form_class = EventEmptyForm
    
    def test_func(self):
        return self.get_event().is_public or self.request.user in self.get_event().invited_volunteers.all()

    def get_event(self):
        return Event.objects.get(pk=self.kwargs['pk'])

    def get_event_pk(self):
        return self.kwargs['pk']

    def form_valid(self, form):
        self.get_event().volunteers.add(self.request.user)
        self.get_event().invited_volunteers.remove(self.request.user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.get_event()
        return context



class EventLeaveView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    login_url = 'login'
    success_url = reverse_lazy('events_public_list')
    template_name = 'events_leave.html'
    form_class = EventEmptyForm
    
    def test_func(self):
        return self.request.user in self.get_event().volunteers.all()

    def get_event(self):
        return Event.objects.get(pk=self.kwargs['pk'])

    def form_valid(self, form):
        self.get_event().volunteers.remove(self.request.user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.get_event()
        return context



class EventRejectInvitationView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    login_url = 'login'
    success_url = reverse_lazy('pending_invitations')
    template_name = 'events_reject_invitation.html'
    form_class = EventEmptyForm

    def test_func(self):
        return self.request.user in self.get_event().invited_volunteers.all()

    def get_event(self):
        return Event.objects.get(pk=self.kwargs['pk'])

    def form_valid(self, form):
        self.get_event().invited_volunteers.remove(self.request.user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.get_event()
        return context

class EventJoinedListView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'events_joined_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['joined_events'] = self.request.user.joined_events.all()
        return context


class EventOrganizerListView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'events_organizer_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organized_events'] = self.request.user.organized_events.all()
        return context


class EventPublicListView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'events_public_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Event.objects.filter(is_public=True)
        return context


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = 'login'
    success_url = reverse_lazy('events_organizer_list')
    template_name = 'events_delete.html'
    model = Event

    def test_func(self):
        event = self.get_object()
        return event.organizer == self.request.user


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = 'login'
    success_url = reverse_lazy('events_organizer_list')
    template_name = 'events_edit.html'
    model = Event
    fields = [
        'name',
        'description',
        'contact',
        'location',
        'spots',
        'is_public',
    ]
    
    def test_func(self):
        event = self.get_object()
        return event.organizer == self.request.user


class EventDetailView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    login_url = 'login'
    template_name = 'events_detail.html'

    def get_event(self):
        return Event.objects.get(pk=self.kwargs['pk'])

    def test_func(self):
        event = self.get_event()
        return event.is_public or self.request.user in self.get_event().invited_volunteers.all() or self.request.user in self.get_event().volunteers.all() or event.organizer == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.get_event()
        return context


class EventAddVolunteersView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    login_url = 'login'
    # success_url = reverse_lazy('project_list', kwargs={'pk': self.kwargs['pk']})
    success_url = reverse_lazy('home')
    template_name = 'events_add_volunteers.html'
    form_class = EventAddVolunteersForm

    def test_func(self):
        return self.get_event().organizer == self.request.user

    def get_event(self):
        return Event.objects.get(pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs

    def form_valid(self, form):
        singular_email_string = form.cleaned_data['email']
        try:
            new_volunteer = get_user_model().objects.get(email=singular_email_string)
            self.get_event().invited_volunteers.add(new_volunteer)
        except:
            pass

        for email_string in [x.strip() for x in form.cleaned_data['emails'].split(',')]:
            try:
                new_volunteer = get_user_model().objects.get(email=email_string)
                self.get_event().invited_volunteers.add(new_volunteer)
            except:
                pass

        return super().form_valid(form)
