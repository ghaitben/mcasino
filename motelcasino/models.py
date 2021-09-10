from django.db import models

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=100)
    room_number = models.IntegerField()
    checkin = models.DateTimeField(blank=True, null=True)
    checkout = models.DateTimeField(blank=True, null=True)

class history(models.Model):
    name = models.CharField(max_length=100)
    room_number = models.IntegerField()
    checkin = models.DateTimeField(blank=True, null=True)
    checkout = models.DateTimeField(blank=True, null=True)
