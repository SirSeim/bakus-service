import typing
from collections import UserList

from attrs import define, fields_dict

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
