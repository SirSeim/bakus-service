import pathlib

from attrs import define, field
from transmission_rpc.lib_types import File as TorrentFile

from addition import enums


@define
class Torrent:
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

    def get_json(self) -> dict:
        return {
            "id": self.id,
            "state": enums.State.DOWNLOADING,
            "name": self.name,
            "progress": self.progress,
            "files": [
                {
                    "name": file.name,
                    "file_type": enums.FileType.VIDEO,
                }
                for file in self.files()
            ],
        }


TORRENT_DICT = {
    "1": Torrent(
        id="1",
        name="test_torrent_1",
        progress=0.05,
    ),
    "2": Torrent(
        id="2",
        name="test_torrent_2",
        progress=0.10,
    ),
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

    def get_json(self) -> dict:
        if self.single_file:
            files = [
                DownloadFile(name=self.name, file_type=enums.FileType.VIDEO).get_json(),
            ]
        else:
            files = [file.get_json() for file in self.files]
        return {
            "id": self.name,
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


DOWNLOADS = [
    Download(
        name="cat-dog.mkv",
        single_file=True,
    ),
    Download(
        name="downloaded-content",
        files=[
            DownloadFile(name="subtitles.srt", file_type=enums.FileType.SUBTITLE),
            DownloadFile(name="poster.jpg", file_type=enums.FileType.IMAGE),
            DownloadFile(name="videos/completed.mov", file_type=enums.FileType.VIDEO),
        ],
    ),
]

USER_USERNAME = "test"
USER_PASSWORD = "test1test"
USER_LOGIN = {
    "username": USER_USERNAME,
    "password": USER_PASSWORD,
}
