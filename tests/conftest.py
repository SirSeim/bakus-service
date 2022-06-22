import pytest
from rest_framework.test import APIClient

from addition import clients
from tests import test_constants


@pytest.fixture
def api_client():
    return APIClient()


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
    monkeypatch.setattr(clients.Transmission, "client", MockTransmission)
