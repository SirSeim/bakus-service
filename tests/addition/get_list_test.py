import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from addition import enums
from tests import test_constants


def expected_results(sort: str = "name") -> list[dict]:
    torrents = [
        {
            "id": torrent.id,
            "state": enums.State.DOWNLOADING,
            "name": torrent.name,
            "progress": torrent.progress,
            "files": [
                {
                    "name": f"{torrent.name}-{num}.mov",
                    "file_type": enums.FileType.VIDEO,
                }
                for num in range(2)
            ],
        }
        for torrent in test_constants.TORRENT_DICT.values()
    ]
    downloaded = [completed for completed in test_constants.DOWNLOADED_DICT.values()]
    return sorted((downloaded + torrents), key=lambda a: a[sort])


@pytest.mark.django_db
def test_get_list(api_client, incoming_folder):
    for name, download in test_constants.DOWNLOADED_DICT.items():
        for file_json in download["files"]:
            file = incoming_folder / name / file_json["name"]
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text("testing")
    response = api_client.get(reverse("addition-list"))
    assert response.status_code == status.HTTP_200_OK
    expected = expected_results()
    assert response.data.get("count") == len(expected)
    assert response.data.get("results") == expected
