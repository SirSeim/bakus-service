import copy
import pathlib

import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from addition import clients, models
from tests import test_constants, test_models


@pytest.fixture
def api_client() -> APIClient:
    User.objects.create_user(username=test_constants.USER_USERNAME, password=test_constants.USER_PASSWORD)
    client = APIClient()
    res = client.post(reverse("knox_login"), test_constants.USER_LOGIN)
    assert res.status_code == status.HTTP_200_OK
    client.credentials(HTTP_AUTHORIZATION=f"Token {res.data['token']}")
    return client


@pytest.fixture
def demo_api_client() -> APIClient:
    user = User.objects.create_user(username=test_constants.DEMO_USERNAME, password=test_constants.DEMO_PASSWORD)
    models.UserSettings.objects.create(user=user, demo=True)
    client = APIClient()
    res = client.post(reverse("knox_login"), test_constants.DEMO_LOGIN)
    assert res.status_code == status.HTTP_200_OK
    client.credentials(HTTP_AUTHORIZATION=f"Token {res.data['token']}")
    return client


class MockTransmission:
    TORRENT_DICT = test_constants.TORRENT_DICT

    @classmethod
    def add_torrent(cls, _: str) -> test_models.Torrent:
        return cls.TORRENT_DICT["1"]

    @classmethod
    def get_torrent(cls, torrent_id: str) -> test_models.Torrent:
        return cls.TORRENT_DICT[torrent_id]

    @classmethod
    def get_torrents(cls) -> list[test_models.Torrent]:
        return [torrent for torrent in cls.TORRENT_DICT.values()]

    @classmethod
    def remove_torrent(cls, torrent_id: int, **_):
        del cls.TORRENT_DICT[str(torrent_id)]


@pytest.fixture(autouse=True)
def mock_transmission_client(monkeypatch):
    # Reset client contents for every test
    MockTransmission.TORRENT_DICT = copy.deepcopy(test_constants.TORRENT_DICT)
    monkeypatch.setattr(clients.Transmission, "_client", MockTransmission)
    return MockTransmission


@pytest.fixture(autouse=True)
def mock_project_folders(tmp_path, settings) -> dict[str, pathlib.Path]:
    incoming = tmp_path / "incoming"
    incoming.mkdir()
    settings.INCOMING_FOLDER = incoming.resolve()
    plex = tmp_path / "plex"
    plex.mkdir()
    settings.PLEX_FOLDER = plex.resolve()
    # Setup Plex folders
    (plex / clients.FileSystem.MOVIES_FOLDER).mkdir()
    (plex / clients.FileSystem.TV_SHOWS_FOLDER).mkdir()
    return {
        "incoming": incoming,
        "plex": plex,
    }


@pytest.fixture
def incoming_folder(mock_project_folders) -> pathlib.Path:
    return mock_project_folders["incoming"]


@pytest.fixture
def plex_folder(mock_project_folders) -> pathlib.Path:
    return mock_project_folders["plex"]
