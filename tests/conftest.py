import pathlib

import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from addition import clients
from tests import test_constants


@pytest.fixture
def api_client() -> APIClient:
    User.objects.create_user(username=test_constants.USER_USERNAME, password=test_constants.USER_PASSWORD)
    client = APIClient()
    res = client.post(reverse("knox_login"), test_constants.USER_LOGIN)
    assert res.status_code == status.HTTP_200_OK
    client.credentials(HTTP_AUTHORIZATION=f"Token {res.data['token']}")
    return client


class MockTransmission:
    @staticmethod
    def add_torrent(_: str) -> test_constants.Torrent:
        return test_constants.TORRENT_DICT["1"]

    @staticmethod
    def get_torrent(torrent_id: str) -> test_constants.Torrent:
        return test_constants.TORRENT_DICT[torrent_id]

    @staticmethod
    def get_torrents() -> list[test_constants.Torrent]:
        return [torrent for torrent in test_constants.TORRENT_DICT.values()]


@pytest.fixture(autouse=True)
def mock_transmission_client(monkeypatch):
    monkeypatch.setattr(clients.Transmission, "_client", MockTransmission)


@pytest.fixture(autouse=True)
def mock_project_folders(tmp_path: pathlib.Path, settings):
    incoming = tmp_path / "incoming"
    incoming.mkdir()
    settings.INCOMING_FOLDER = incoming.resolve()
    plex = tmp_path / "plex"
    plex.mkdir()
    settings.PLEX_FOLDER = plex.resolve()
