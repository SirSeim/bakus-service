from attrs import define
from django.db import models

from addition import enums


@define
class Addition:
    id: str
    state: enums.State
    name: str
    progress: float
