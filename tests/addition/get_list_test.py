import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from addition import enums
from tests import test_constants, test_models


def expected_results(sort: str = "name") -> list[dict]:
    torrents = [torrent.get_json() for torrent in test_constants.TORRENT_DICT.values()]
    downloaded = [completed.get_json() for completed in test_constants.DOWNLOADS]
    return sorted((downloaded + torrents), key=lambda a: a[sort])


@pytest.mark.django_db
def test_get_list(api_client, incoming_folder):
    for download in test_constants.DOWNLOADS:
        download.create_files(incoming_folder)
    response = api_client.get(reverse("addition-list"))
    assert response.status_code == status.HTTP_200_OK
    expected = expected_results()
    assert response.data.get("count") == len(expected)
    assert response.data.get("results") == expected


DOWNLOADS_TO_EXCLUDE = [
    ("", test_models.Download(name="text-file.txt", single_file=True)),
    (
        "backlog",
        test_models.Download(
            name="backlog",
            files=[
                test_models.DownloadFile(name="first.mov", file_type=enums.FileType.VIDEO),
                test_models.DownloadFile(name="second.mov", file_type=enums.FileType.VIDEO),
            ],
        ),
    ),
    ("", test_models.Download(name="temp.mov.part", single_file=True)),
    (
        "",
        test_models.Download(
            name="missing-video",
            files=[
                test_models.DownloadFile(name="text-file.txt", file_type=enums.FileType.OTHER),
                test_models.DownloadFile(name="subtitle.srt", file_type=enums.FileType.SUBTITLE),
                test_models.DownloadFile(name="image.jpg", file_type=enums.FileType.IMAGE),
            ],
        ),
    ),
]


@pytest.mark.django_db
@pytest.mark.parametrize("ignore_file,download", DOWNLOADS_TO_EXCLUDE)
def test_exclude_partials(api_client, incoming_folder, mock_transmission_client, ignore_file, download, settings):
    # stop including torrents
    mock_transmission_client.TORRENT_DICT = {}

    if ignore_file:
        settings.EXCLUDE_NAMES = {ignore_file}
    download.create_files(incoming_folder)
    response = api_client.get(reverse("addition-list"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("count") == 0
    assert response.data.get("results") == []


# TODO: Add test combining list and detail calls
