from __future__ import unicode_literals

from django.db import models

class GardenImages(models.Model):
        name = models.CharField(max_length=50)
        imageData = models.TextField()
        createdAt = models.DateField(auto_now_add=True)
        updatedAt = models.DateField(auto_now=True)
        
class DataFile(models.Model):
	data = models.FileField()
