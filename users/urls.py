from django.urls import path

from .views import SignUpView, PendingInvitationsListView


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('pending_invitations', PendingInvitationsListView.as_view(), name='pending_invitations'),
]