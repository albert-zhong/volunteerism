from django.urls import path

from .views import (
    EventCreateView,
    EventDeleteView,
    EventPublicListView,
    EventOrganizerListView,
    EventJoinedListView,
    EventJoinView,
    EventLeaveView,
    EventUpdateView,
    EventDetailView,
    EventAddVolunteersView,
    EventRejectInvitationView,
)

urlpatterns = [
    path('<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('<int:pk>/join/', EventJoinView.as_view(), name='event_join'),
    path('<int:pk>/leave/', EventLeaveView.as_view(), name='event_leave'),
    path('<int:pk>/reject/', EventRejectInvitationView.as_view(), name='event_reject_invitation'),
    path('<int:pk>/edit/', EventUpdateView.as_view(), name='event_update'),
    path('<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),
    path('<int:pk>/add_volunteers/', EventAddVolunteersView.as_view(), name='event_add_volunteers'),
    path('public/', EventPublicListView.as_view(), name='events_public_list'),
    path('organizer/', EventOrganizerListView.as_view(), name='events_organizer_list'),
    path('joined/', EventJoinedListView.as_view(), name='events_joined_list'),
    path('new/', EventCreateView.as_view(), name='events_new'),
]