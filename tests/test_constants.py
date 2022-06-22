from attrs import define


@define
class Torrent:
    id: str
    name: str
    progress: float


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
