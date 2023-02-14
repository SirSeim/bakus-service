import os
import pathlib

from django.conf import settings
from transmission_rpc import Client, Torrent
from transmission_rpc.lib_types import File as TorrentFile

from addition import enums, models
from common import hash_id


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
        return cls.format_addition(torrent)

    @classmethod
    def get_torrents(cls) -> models.AdditionSet[models.Addition]:
        return models.AdditionSet([cls.format_addition(torrent) for torrent in cls.client().get_torrents()])

    @classmethod
    def format_addition(cls, torrent: Torrent) -> models.Addition:
        files = [cls.format_file(f) for f in torrent.files()]
        files.sort(key=lambda f: f.name)
        return models.Addition(
            id=hash_id(str(torrent.id)),
            state=enums.State.DOWNLOADING,
            name=torrent.name,
            progress=torrent.progress / 100,
            files=files,
        )

    @staticmethod
    def format_file(file: TorrentFile) -> models.File:
        file_parts = pathlib.Path(file.name).parts
        if len(file_parts) == 1:
            name = file_parts[0]
        else:
            name = str(pathlib.Path(*file_parts[1:]))
        return models.File(
            name=name,
            file_type=enums.FileType.get_extension(pathlib.Path(file.name)),
        )


class FileSystem:
    @classmethod
    def get_files(cls) -> models.AdditionSet[models.Addition]:
        res = []
        for addition in pathlib.Path(settings.INCOMING_FOLDER).iterdir():
            if addition.name in settings.EXCLUDE_NAMES:
                continue
            # Add single file cases
            if addition.is_file():
                a = models.Addition(
                    state=enums.State.COMPLETED,
                    name=addition.name,
                    progress=1.0,
                    files=[cls.format_file(pathlib.Path(addition.name))],
                )
                if a.is_valid():
                    res.append(a)
                continue
            # Add multi-file cases
            addition_files = []
            for root, _, files in os.walk(str(addition)):
                for f in files:
                    if f in settings.EXCLUDE_NAMES:
                        continue
                    file_name = pathlib.Path(root, f).relative_to(addition)
                    addition_files.append(cls.format_file(file_name))
            addition_files.sort(key=lambda f: f.name)
            a = models.Addition(
                state=enums.State.COMPLETED,
                name=addition.name,
                progress=1.0,
                files=addition_files,
            )
            if a.is_valid():
                res.append(a)
        return models.AdditionSet(res)

    @staticmethod
    def format_file(file: pathlib.Path) -> models.File:
        return models.File(
            name=str(file),
            file_type=enums.FileType.get_extension(file),
        )
