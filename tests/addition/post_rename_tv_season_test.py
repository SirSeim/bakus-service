import json

import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from addition import enums
from addition.clients import FileSystem
from tests import test_constants


@pytest.mark.django_db
def test_single_file(api_client, incoming_folder, plex_folder):
    test_constants.SINGLE_DOWNLOAD.create_files(incoming_folder)
    payload = {
        "title": test_constants.SINGLE_TITLE,
        "season": 1,
        "files": [
            {
                "current_name": test_constants.SINGLE_DOWNLOAD.name,
                "new_name": f"{test_constants.SINGLE_TITLE}.mkv",
            }
        ],
    }
    response = api_client.post(
        reverse("addition-rename-tv-season", args=[test_constants.SINGLE_DOWNLOAD.external_id]),
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_200_OK
    payload["delete_rest"] = False
    assert response.data == payload

    old_file = incoming_folder / test_constants.SINGLE_DOWNLOAD.name
    assert not old_file.exists(), "old file should no longer be there"
    new_file = (
        plex_folder
        / FileSystem.TV_SHOWS_FOLDER
        / test_constants.SINGLE_TITLE
        / "Season 01"
        / f"{test_constants.SINGLE_TITLE}.mkv"
    )
    assert new_file.exists() and new_file.is_file(), "file should now be here"


def file_type_to_extension(file_type: enums.FileType) -> str:
    if file_type == enums.FileType.VIDEO:
        return "mov"
    elif file_type == enums.FileType.SUBTITLE:
        return "srt"
    elif file_type == enums.FileType.IMAGE:
        return "jpg"
    return "txt"


@pytest.mark.django_db
def test_multiple_files_move_everything(api_client, incoming_folder, plex_folder):
    test_constants.DIR_DOWNLOAD.create_files(incoming_folder)
    payload = {
        "title": test_constants.DIR_TITLE,
        "season": 1,
        "files": [
            {
                "current_name": file.name,
                "new_name": f"{test_constants.DIR_TITLE}.{file_type_to_extension(file.file_type)}",
            }
            for file in test_constants.DIR_DOWNLOAD.files
        ],
    }
    response = api_client.post(
        reverse("addition-rename-tv-season", args=[test_constants.DIR_DOWNLOAD.external_id]),
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_200_OK
    payload["delete_rest"] = False
    assert response.data == payload

    old_dir = incoming_folder / test_constants.DIR_DOWNLOAD.name
    assert not old_dir.exists(), "old dir should no longer be there"
    for file in test_constants.DIR_DOWNLOAD.files:
        new_file = (
            plex_folder
            / FileSystem.TV_SHOWS_FOLDER
            / test_constants.DIR_TITLE
            / "Season 01"
            / f"{test_constants.DIR_TITLE}.{file_type_to_extension(file.file_type)}"
        )
        assert new_file.exists() and new_file.is_file(), "file should now be here"


@pytest.mark.django_db
def test_multiple_files_leave_some_behind(api_client, incoming_folder, plex_folder):
    test_constants.DIR_DOWNLOAD.create_files(incoming_folder)
    file_to_move = [file for file in test_constants.DIR_DOWNLOAD.files if file.file_type == enums.FileType.VIDEO][0]
    payload = {
        "title": test_constants.DIR_TITLE,
        "season": 1,
        "files": [
            {
                "current_name": file_to_move.name,
                "new_name": f"{test_constants.DIR_TITLE}.mov",
            }
        ],
    }
    response = api_client.post(
        reverse("addition-rename-tv-season", args=[test_constants.DIR_DOWNLOAD.external_id]),
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_200_OK
    payload["delete_rest"] = False
    assert response.data == payload

    old_dir = incoming_folder / test_constants.DIR_DOWNLOAD.name
    assert old_dir.exists(), "old dir should be there"
    for file in test_constants.DIR_DOWNLOAD.files:
        new_file = (
            plex_folder
            / FileSystem.TV_SHOWS_FOLDER
            / test_constants.DIR_TITLE
            / "Season 01"
            / f"{test_constants.DIR_TITLE}.{file_type_to_extension(file.file_type)}"
        )
        old_file = old_dir / file.name
        # only the video file was sent for renaming
        if file.file_type == enums.FileType.VIDEO:
            assert new_file.exists() and new_file.is_file(), "file should now be here"
            assert not old_file.exists(), "file should no longer be in old location"
        else:
            assert not new_file.exists(), "file should not have been moved"
            assert old_file.exists() and old_file.is_file(), "file should have stayed in original location"


@pytest.mark.django_db
def test_multiple_files_clear_old(api_client, incoming_folder, plex_folder):
    test_constants.DIR_DOWNLOAD.create_files(incoming_folder)
    file_to_move = [file for file in test_constants.DIR_DOWNLOAD.files if file.file_type == enums.FileType.VIDEO][0]
    payload = {
        "title": test_constants.DIR_TITLE,
        "season": 1,
        "delete_rest": True,
        "files": [
            {
                "current_name": file_to_move.name,
                "new_name": f"{test_constants.DIR_TITLE}.mov",
            }
        ],
    }
    response = api_client.post(
        reverse("addition-rename-tv-season", args=[test_constants.DIR_DOWNLOAD.external_id]),
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data == payload

    old_dir = incoming_folder / test_constants.DIR_DOWNLOAD.name
    assert not old_dir.exists(), "old dir should not be there"
    for file in test_constants.DIR_DOWNLOAD.files:
        new_file = (
            plex_folder
            / FileSystem.TV_SHOWS_FOLDER
            / test_constants.DIR_TITLE
            / "Season 01"
            / f"{test_constants.DIR_TITLE}.{file_type_to_extension(file.file_type)}"
        )
        old_file = old_dir / file.name
        # only the video file was sent for renaming
        if file.file_type == enums.FileType.VIDEO:
            assert new_file.exists() and new_file.is_file(), "file should now be here"
        assert not old_file.exists(), "file should no longer be in old location"


# TODO: Add test for assuring in-progress Additions cannot be renamed
