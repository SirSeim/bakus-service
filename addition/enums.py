from django.db import models


class AdditionType(models.TextChoices):
    MOVIE = "MO", "Movie"
    TV_SHOW = "TV", "TV Show"
