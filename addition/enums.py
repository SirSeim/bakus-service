from django.db import models


class State(models.TextChoices):
    DOWNLOADING = "DW", "Downloading"
    COMPLETED = "CP", "Completed"
