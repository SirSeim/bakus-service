from django.db import models


class State(models.TextChoices):
    DOWNLOADING = "DW", "Downloading"
    COMPLETED = "CP", "Completed"


class FileType(models.TextChoices):
    VIDEO = "VID", "Video"
    SUBTITLE = "SUB", "Subtitle"
    IMAGE = "IMG", "Image"
    OTHER = "OTH", "Other"
