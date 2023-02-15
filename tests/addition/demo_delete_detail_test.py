import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from common import hash_id
from tests import test_constants


@pytest.mark.django_db
def test_demo_delete_detail(demo_api_client, mock_transmission_client, incoming_folder):
    for download in test_constants.DOWNLOADS:
        download.create_files(incoming_folder)
    response = demo_api_client.delete(reverse("addition-detail", args=[hash_id("non-existent")]))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # Nothing was actually deleted
    assert len(list(incoming_folder.iterdir())) == len(test_constants.DOWNLOADS)
    assert len(mock_transmission_client.TORRENT_DICT) == len(test_constants.TORRENT_DICT)


ADDITION_LIST = [(True, a) for a in test_constants.TORRENT_DICT.values()] + [
    (False, a) for a in test_constants.DOWNLOADS
]


@pytest.mark.django_db
@pytest.mark.parametrize("is_torrent,addition", ADDITION_LIST)
def test_demo_delete_detail_validate_all_cases(
    demo_api_client, mock_transmission_client, incoming_folder, is_torrent, addition
):
    for download in test_constants.DOWNLOADS:
        download.create_files(incoming_folder)

    response = demo_api_client.delete(reverse("addition-detail", args=[addition.external_id]))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # Nothing was actually deleted
    assert len(list(incoming_folder.iterdir())) == len(test_constants.DOWNLOADS)
    assert len(mock_transmission_client.TORRENT_DICT) == len(test_constants.TORRENT_DICT)
