import typing
from collections import UserList

from attrs import define, fields_dict
from django.db import models

from addition import enums


@define
class Addition:
    id: str
    state: enums.State
    name: str
    progress: float

    @classmethod
    def fields(cls) -> typing.List[str]:
        return list(fields_dict(cls))


class ObjectSet(UserList):
    def order_by(self, *ordering: str) -> "ObjectSet":
        res = self.data
        for o in reversed(ordering):
            reverse = o.startswith("-")
            if reverse:
                o = o[1:]
            res = sorted(res, key=lambda x: getattr(x, o), reverse=reverse)
        return ObjectSet(res)
