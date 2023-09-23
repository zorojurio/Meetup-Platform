from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    even_tribe_id = models.CharField(max_length=255)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    venue = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    ticket_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    is_free = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} {self.pk}'
