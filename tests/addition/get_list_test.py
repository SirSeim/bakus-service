import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from tests import test_constants


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
