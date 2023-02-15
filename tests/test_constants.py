from addition import enums
from tests.test_models import Download, DownloadFile, Torrent

TORRENT_DICT = {
    "1": Torrent(
        id="1",
        name="test_torrent_1",
        progress=5.0,
    ),
    "2": Torrent(
        id="2",
        name="test_torrent_2",
        progress=10.0,
    ),
}


SINGLE_DOWNLOAD = Download(
    name="cat-dog.mkv",
    single_file=True,
)
DIR_DOWNLOAD = Download(
    name="downloaded-content",
    files=[
        DownloadFile(name="poster.jpg", file_type=enums.FileType.IMAGE),
        DownloadFile(name="subtitles.srt", file_type=enums.FileType.SUBTITLE),
        DownloadFile(name="videos/completed.mov", file_type=enums.FileType.VIDEO),
    ],
)


DOWNLOADS = [
    SINGLE_DOWNLOAD,
    DIR_DOWNLOAD,
]

SINGLE_TITLE = "Cat Dog (year)"
DIR_TITLE = "Download Content (year)"

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
