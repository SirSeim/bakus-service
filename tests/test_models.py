import pathlib

from attrs import define, field
from transmission_rpc.lib_types import File as TorrentFile

from addition import enums
from common import hash_id


@define
class Torrent:
    """
    Torrent represents the data that would come out of the Transmission-RPC client.
    It has helper functions that generate the expected output in the endpoint
    """

    id: str
    name: str
    progress: float

    def files(self) -> list[TorrentFile]:
        return [self.create_file(i) for i in range(2)]

    def create_file(self, num: int) -> TorrentFile:
        return TorrentFile(
            name=f"{self.name}-{num}.mov",
            size=500000,
            completed=455761,
            priority="normal",
            selected=True,
        )

    @property
    def external_id(self) -> str:
        return str(hash_id(self.id))

    def get_json(self, include_files=True) -> dict:
        files = []
        if include_files:
            files = self.files()
        return {
            "id": self.external_id,
            "state": enums.State.DOWNLOADING,
            "name": self.name,
            "progress": self.progress / 100,
            "files": [
                {
                    "name": file.name,
                    "file_type": enums.FileType.VIDEO,
                }
                for file in files
            ],
        }


@define
class DownloadFile:
    name: str
    file_type: enums.FileType

    def get_json(self) -> dict:
        return {
            "name": self.name,
            "file_type": self.file_type,
        }


@define
class Download:
    name: str
    single_file: bool = field(default=False)
    files: list[DownloadFile] = field(default=[])

    @property
    def external_id(self) -> str:
        return str(hash_id(self.name))

    def get_json(self) -> dict:
        if self.single_file:
            files = [
                DownloadFile(name=self.name, file_type=enums.FileType.VIDEO).get_json(),
            ]
        else:
            files = [file.get_json() for file in self.files]
        return {
            "id": self.external_id,
            "state": enums.State.COMPLETED,
            "name": self.name,
            "progress": 1.0,
            "files": files,
        }

    def create_files(self, path: pathlib.Path):
        if self.single_file:
            file = path / self.name
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text("testing")
        else:
            for file_data in self.files:
                file = path / self.name / file_data.name
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text("testing")
