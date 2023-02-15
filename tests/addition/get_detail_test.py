import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from common import hash_id
from tests import test_constants


def expected_results(id_: str = test_constants.SINGLE_DOWNLOAD.external_id) -> dict:
    torrents = [torrent.get_json() for torrent in test_constants.TORRENT_DICT.values()]
    downloaded = [completed.get_json() for completed in test_constants.DOWNLOADS]
    for addition in downloaded + torrents:
        if addition["id"] == id_:
            return addition
    raise LookupError(f"no test instance exists with id: {id_}")


@pytest.mark.django_db
def test_get_detail(api_client, incoming_folder):
    for download in test_constants.DOWNLOADS:
        download.create_files(incoming_folder)
    response = api_client.get(reverse("addition-detail", args=[test_constants.SINGLE_DOWNLOAD.external_id]))
    assert response.status_code == status.HTTP_200_OK
    expected = expected_results()
    assert response.data == expected


@pytest.mark.django_db
def test_get_detail_not_found(api_client):
    response = api_client.get(reverse("addition-detail", args=[hash_id("non-existent")]))
    assert response.status_code == status.HTTP_404_NOT_FOUND
