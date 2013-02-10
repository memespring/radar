from django.db import models
from json_field import JSONField
from django.db.models.signals import post_save

class EventType(models.Model):
    short_name = models.CharField(max_length = 100, null=False, blank=False)
    display_name = models.CharField(max_length = 100, null=False, blank=False)

    def __str__(self):
      return self.display_name


class Event(models.Model):
    class Meta:
        ordering = ['-created']

    message = models.CharField(max_length = 255, null=False, blank=False)
    event_type = models.ForeignKey(EventType)
    info_link = models.URLField(null=True, blank=False)
    action_link = models.URLField(null=True, blank=True)
    guid = models.CharField(max_length = 255, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    occured = models.DateTimeField(null=True)
    address = models.CharField(max_length = 255, null=True, blank=False)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    data = JSONField()

    def __str__(self):
      return self.event_type.display_name + ' - ' + self.message

class Alert(models.Model):
    event = models.ForeignKey(Event)


def event_created(sender, instance, created, **kwargs):
    if created:
        alert = Alert()
        alert.event = instance
        alert.save()

post_save.connect(event_created, sender=Event)
