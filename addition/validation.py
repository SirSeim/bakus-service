import os

from django.conf import settings
from rest_framework.exceptions import ValidationError


def addition_exists(name: str):
    if not os.path.exists(os.path.join(settings.INCOMING_FOLDER, name)):
        raise ValidationError(f"({name}) is not present for importing")
