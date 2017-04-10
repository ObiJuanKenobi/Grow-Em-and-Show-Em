from __future__ import unicode_literals

from django.db import models
from django import forms
from django.core.urlresolvers import reverse


class GardenImages(models.Model):
    Bed_Name = models.CharField(max_length=120)
    Bed_Plan = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.Bed_Name

    def __str__(self):
        return self.Bed_Name

    def get_absolute_url(self):
        return reverse("bed:details", kwargs={"id": self.id})

    class Meta:
        ordering = ["-timestamp", "-updated"]


class DataFile(models.Model):
    data = models.FileField()
