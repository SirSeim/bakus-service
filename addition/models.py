import typing
from collections import UserList

from attrs import define, fields_dict
from django.contrib.auth.models import User
from django.db import models

from addition import enums


@define
class File:
    name: str
    file_type: enums.FileType


@define
class Addition:
    id: str
    state: enums.State
    name: str
    progress: float
    files: list[File]

    @classmethod
    def fields(cls) -> typing.List[str]:
        return list(fields_dict(cls))

    def is_valid(self) -> bool:
        # any partial files means not valid
        if any(file.file_type == enums.FileType.PARTIAL for file in self.files):
            return False
        # must have video to be valid
        return any(file.file_type == enums.FileType.VIDEO for file in self.files)


class ObjectSet(UserList):
    def filter(self, **kwargs: list) -> "ObjectSet":
        res = self.data
        for key, val in kwargs.items():
            # TODO: once AttributeFilter returns correct value types, stop string converting
            res = filter(lambda addition: str(getattr(addition, key)) in val, res)
        return ObjectSet(res)

    def order_by(self, *ordering: str) -> "ObjectSet":
        res = self.data
        for o in reversed(ordering):
            reverse = o.startswith("-")
            if reverse:
                o = o[1:]
            res = sorted(res, key=lambda x: getattr(x, o), reverse=reverse)
        return ObjectSet(res)


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="settings")
    demo = models.BooleanField(default=False, null=False)


def get_user_settings(user: User) -> UserSettings:
    try:
        return user.settings
    except User.settings.RelatedObjectDoesNotExist:
        pass
    return UserSettings()
