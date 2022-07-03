from attrs import define
from transmission_rpc.lib_types import File as TorrentFile


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

USER_USERNAME = "test"
USER_PASSWORD = "test1test"
USER_LOGIN = {
    "username": USER_USERNAME,
    "password": USER_PASSWORD,
}
