import pathlib

from django.db import models


class State(models.TextChoices):
    DOWNLOADING = "DW", "Downloading"
    COMPLETED = "CP", "Completed"


class FileType(models.TextChoices):
    VIDEO = "VID", "Video"
    SUBTITLE = "SUB", "Subtitle"
    IMAGE = "IMG", "Image"
    PARTIAL = "PRT", "Partial"
    OTHER = "OTH", "Other"

    @staticmethod
    def get_extension(file: pathlib.Path) -> "FileType":
        ext = file.suffix.strip(".").lower()
        if ext == "part":
            return FileType.PARTIAL
        elif ext in ("asf", "avi", "mov", "mp4", "mpeg", "mpegts", "ts", "mkv", "wmv"):
            return FileType.VIDEO
        elif ext in ("srt", "smi", "ssa", "ass", "vtt"):
            return FileType.SUBTITLE
        elif ext in ("jpg", "jpeg", "png"):
            return FileType.IMAGE
        return FileType.OTHER
