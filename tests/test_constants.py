from addition import enums
from tests.test_models import Download, DownloadFile, Torrent

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


DOWNLOADS = [
    Download(
        name="cat-dog.mkv",
        single_file=True,
    ),
    Download(
        name="downloaded-content",
        files=[
            DownloadFile(name="poster.jpg", file_type=enums.FileType.IMAGE),
            DownloadFile(name="subtitles.srt", file_type=enums.FileType.SUBTITLE),
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

DEMO_USERNAME = "demo"
DEMO_PASSWORD = "demo1demo"
DEMO_LOGIN = {
    "username": DEMO_USERNAME,
    "password": DEMO_PASSWORD,
}

ALT_USERNAME = "adamexample"
ALT_EMAIL = "adam@example.io"
ALT_FIRST_NAME = "Adam"
ALT_LAST_NAME = "Example"

ALT_USER_DETAILS = {
    "username": ALT_USERNAME,
    "email": ALT_EMAIL,
    "first_name": ALT_FIRST_NAME,
    "last_name": ALT_LAST_NAME,
}
