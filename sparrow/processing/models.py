from django.db import models


class Valuta(models.Model):
    value = models.IntegerField()
    currency = models.CharField(max_length=8)
    date = models.CharField(max_length=8)
