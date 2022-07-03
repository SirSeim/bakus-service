import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from addition import enums
from tests import test_constants


@pytest.mark.django_db
def test_get_list(api_client):
    response = api_client.get(reverse("addition-list"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("count") == len(test_constants.TORRENT_DICT)
    assert response.data.get("results") == [
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
