import json

import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from addition.clients import FileSystem
from tests import test_constants


@pytest.mark.django_db
@pytest.mark.parametrize("delete_rest", [False, True])
def test_nothing_changes(demo_api_client, incoming_folder, plex_folder, delete_rest):
    test_constants.SINGLE_DOWNLOAD.create_files(incoming_folder)
    payload = {
        "title": test_constants.SINGLE_TITLE,
        "delete_rest": delete_rest,
        "files": [
            {
                "current_name": test_constants.SINGLE_DOWNLOAD.name,
                "new_name": f"{test_constants.SINGLE_TITLE}.mkv",
            }
        ],
    }
    response = demo_api_client.post(
        reverse("addition-rename-movie", args=[test_constants.SINGLE_DOWNLOAD.external_id]),
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data == payload

    old_file = incoming_folder / test_constants.SINGLE_DOWNLOAD.name
    assert old_file.exists() and old_file.is_file(), "old file should still be there"
    new_file = (
        plex_folder / FileSystem.MOVIES_FOLDER / test_constants.SINGLE_TITLE / f"{test_constants.SINGLE_TITLE}.mkv"
    )
    assert not new_file.exists(), "file should not have moved here"
