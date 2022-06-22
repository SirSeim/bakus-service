import os

from django.conf import settings
from transmission_rpc import Client

from addition import enums, models


class Transmission:
    _client = None

    @classmethod
    def client(cls) -> Client:
        if not getattr(cls, "_client", None):
            cls._client = Client(
                host=settings.TRANSMISSION_HOST,
                port=settings.TRANSMISSION_PORT,
                username=settings.TRANSMISSION_USERNAME,
                password=settings.TRANSMISSION_PASSWORD,
            )
        return cls._client

    @classmethod
    def add_torrent(cls, magnet_link: str) -> models.Addition:
        torrent = cls.client().add_torrent(magnet_link)
        # Errors occur accessing properties without refreshing object first
        torrent = cls.client().get_torrent(torrent_id=torrent.id)
        return models.Addition(
            id=torrent.id,
            state=enums.State.DOWNLOADING,
            name=torrent.name,
            progress=torrent.progress,
        )

    @classmethod
    def get_torrents(cls) -> models.ObjectSet[models.Addition]:
        return models.ObjectSet(
            [
                models.Addition(
                    id=torrent.id,
                    state=enums.State.DOWNLOADING,
                    name=torrent.name,
                    progress=torrent.progress,
                )
                for torrent in cls.client().get_torrents()
            ]
        )


class FileSystem:
    @staticmethod
    def get_files() -> models.ObjectSet[models.Addition]:
        return models.ObjectSet(
            [
                # TODO: set a reliable ID
                models.Addition(
                    id=os.path.basename(os.path.normpath(file[0])),
                    state=enums.State.COMPLETED,
                    name=os.path.basename(os.path.normpath(file[0])),
                    progress=1.0,
                )
                for file in os.walk(settings.INCOMING_FOLDER)
                if file[0] != settings.INCOMING_FOLDER
            ]
        )
