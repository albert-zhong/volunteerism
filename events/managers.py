from django.db import models
from django.utils.translation import ugettext_lazy as _


class EventManager(models.Manager):
    def create_event(self, name, description, contact, location, spots, is_public, volunteers, organizer):
        new_event = self.model(
            name=name,
            description=description,
            contact=contact,
            location=location,
            spots=spots,
            is_public=is_public,
            volunteers=volunteers,
            organizer=organizer,
        )
        new_event.save()
        return new_event