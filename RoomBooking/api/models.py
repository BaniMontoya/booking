from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone

class Room(models.Model):
    
    last_updated = models.DateTimeField(editable=False, default=timezone.now)
    created = models.DateTimeField( editable=False, default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=None)
    name = models.CharField(max_length=100, default="")
    capacity = models.IntegerField()

    def __str__(self):
        return str(self.pk)


class Event(models.Model):
    
    last_updated = models.DateTimeField(editable=False, default=timezone.now)
    created = models.DateTimeField( editable=False, default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=None)
    name = models.CharField(max_length=100, default="")
    room = models.ForeignKey(Room, on_delete=models.PROTECT, default=None)
    is_private = models.BooleanField(default=False)
    start_date = models.DateField( default=timezone.now)
    end_date = models.DateField( default=timezone.now)
    
    def __str__(self):
        return str(self.pk)


class Booking(models.Model):

    last_updated = models.DateTimeField(editable=False, default=timezone.now)
    created = models.DateTimeField( editable=False, default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=None)
    event = models.ForeignKey(Event, on_delete=models.PROTECT, default=None)

    def __str__(self):
        return str(self.pk)

