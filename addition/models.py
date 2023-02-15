import typing
import uuid
from collections import UserList

from attrs import define, field, fields_dict
from django.contrib.auth.models import User
from django.db import models

from addition import enums, errors
from common import hash_id


@define
class File:
    name: str
    file_type: enums.FileType


@define
class Addition:
    files: list[File]
    name: str
    progress: float
    state: enums.State
    delete: typing.Callable

    id: uuid.UUID = field()

    DoesNotExist = errors.DoesNotExist

    # TODO: This should be done properly.
    class Meta:
        def __init__(self, object_name):
            self.object_name = object_name

    _meta = Meta("Addition")

    @classmethod
    def fields(cls) -> typing.List[str]:
        return list(fields_dict(cls))

    @id.default
    def _id_default(self) -> uuid.UUID:
        return hash_id(self.name)

    def is_valid(self) -> bool:
        # any partial files means not valid
        if any(file.file_type == enums.FileType.PARTIAL for file in self.files):
            return False
        # must have video to be valid
        return any(file.file_type == enums.FileType.VIDEO for file in self.files)


class AdditionSet(UserList):
    model = Addition

    def get(self, **kwargs: dict) -> Addition:
        for d in self.data:
            found = True
            for key, val in kwargs.items():
                if getattr(d, key) != val:
                    found = False
            # TODO: Raise error when multiple match
            if found:
                return d
        raise self.model.DoesNotExist()

    def filter(self, **kwargs: list) -> "AdditionSet[Addition]":
        res = self.data
        for key, val in kwargs.items():
            # TODO: once AttributeFilter returns correct value types, stop string converting
            res = filter(lambda addition: str(getattr(addition, key)) in val, res)
        return AdditionSet(res)

    def order_by(self, *ordering: str) -> "AdditionSet[Addition]":
        res = self.data
        for o in reversed(ordering):
            reverse = o.startswith("-")
            if reverse:
                o = o[1:]
            res = sorted(res, key=lambda x: getattr(x, o), reverse=reverse)
        return AdditionSet(res)


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="settings")
    demo = models.BooleanField(default=False, null=False)


def get_user_settings(user: User) -> UserSettings:
    try:
        return user.settings
    except User.settings.RelatedObjectDoesNotExist:
        pass
    return UserSettings()
