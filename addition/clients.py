import os
import typing

from django.conf import settings
from transmission_rpc import Client

from addition import enums, models


class Transmission:
    client = Client(
        host=settings.TRANSMISSION_HOST,
        port=settings.TRANSMISSION_PORT,
        username=settings.TRANSMISSION_USERNAME,
        password=settings.TRANSMISSION_PASSWORD,
    )

    @classmethod
    def add_torrent(cls, magnet_link: str) -> models.Addition:
        torrent = cls.client.add_torrent(magnet_link)
        return models.Addition(
            id=torrent.id,
            state=enums.State.DOWNLOADING,
            name=torrent.name,
            progress=torrent.progress,
        )

    @classmethod
    def get_torrents(cls) -> typing.List[models.Addition]:
        return [
            models.Addition(
                id=torrent.id,
                state=enums.State.DOWNLOADING,
                name=torrent.name,
                progress=torrent.progress,
            )
            for torrent in cls.client.get_torrents()
        ]


class FileSystem:
    @staticmethod
    def get_files() -> typing.List[models.Addition]:
        return [
            # TODO: set a reliable ID
            models.Addition(
                id=os.path.basename(os.path.normpath(file[0])),
                state=enums.State.COMPLETED,
                name=os.path.basename(os.path.normpath(file[0])),
                progress=1.0,
            )
            for file in [t for t in os.walk(settings.INCOMING_FOLDER) if t[0] != settings.INCOMING_FOLDER]
        ]
