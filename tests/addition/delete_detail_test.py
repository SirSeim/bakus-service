import copy

import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from common import hash_id
from tests import test_constants


@pytest.mark.django_db
@pytest.mark.parametrize("torrent_id", test_constants.TORRENT_DICT)
def test_delete_detail_torrent(api_client, mock_transmission_client, torrent_id):
    response = api_client.delete(reverse("addition-detail", args=[hash_id(torrent_id)]))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert len(mock_transmission_client.TORRENT_DICT) == len(test_constants.TORRENT_DICT) - 1
    assert torrent_id not in mock_transmission_client.TORRENT_DICT


@pytest.mark.django_db
@pytest.mark.parametrize("download", test_constants.DOWNLOADS)
def test_delete_detail_files(api_client, mock_transmission_client, incoming_folder, download):
    # don't include torrents
    mock_transmission_client.TORRENT_DICT = {}
    downloads = copy.deepcopy(test_constants.DOWNLOADS)
    for d in downloads:
        d.create_files(incoming_folder)

    response = api_client.delete(reverse("addition-detail", args=[download.external_id]))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    updated_downloads = list(incoming_folder.iterdir())
    assert len(updated_downloads) == len(downloads) - 1
    assert download.name not in updated_downloads
