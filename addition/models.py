from django.db import models

from addition import enums, validation


class Addition(models.Model):
    name = models.CharField(max_length=255, validators=[validation.addition_exists])
    content_type = models.CharField(max_length=2, choices=enums.AdditionType.choices, default=enums.AdditionType.MOVIE)
