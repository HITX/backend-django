from django.db import models

class Learn(models.Model):
    name = models.CharField(max_length=256)
    type = models.CharField(max_length=256)
    bullshit = models.CharField(max_length=256)
