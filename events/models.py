from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


class Event(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=2048)
    contact = models.CharField(max_length=64)
    location = models.CharField(max_length=64)
    time = models.CharField(max_length=64)
    spots = models.PositiveIntegerField()
    is_public = models.BooleanField()

    invited_volunteers = models.ManyToManyField(
        get_user_model(),
        related_name='pending_invitations',
        blank=True,
    )

    volunteers = models.ManyToManyField(
        get_user_model(),
        related_name='joined_events',
        blank=True,
    )

    organizer = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='organized_events',
    )

    def __str__(self):
        return f"{self.name} at {self.location}"
