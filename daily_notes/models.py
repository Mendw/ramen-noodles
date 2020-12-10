from django.db import models
from django.core import validators

class Goal(models.Model):
    year = models.SmallIntegerField(validators=[
        validators.MinValueValidator(2019),
        validators.MaxValueValidator(2099)
    ])

    month = models.SmallIntegerField(validators=[
        validators.MinValueValidator( 1),
        validators.MaxValueValidator(12)
    ])

    title = models.CharField(max_length=255,validators=[
        validators.MinLengthValidator(5)
    ])

    content = models.TextField(blank=True)

class Day(models.Model):
    date = models.DateField(primary_key=True)
    activities = models.TextField()



