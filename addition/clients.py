import os

from django.conf import settings
from transmission_rpc import Client, Torrent

from addition import enums, models


def get_file_extension(file: str) -> enums.FileType:
    ext = os.path.splitext(file)[1].strip(".").lower()
    if ext in ("asf", "avi", "mov", "mp4", "mpeg", "mpegts", "ts", "mkv", "wmv"):
        return enums.FileType.VIDEO
    elif ext in ("srt", "smi", "ssa", "ass", "vtt"):
        return enums.FileType.SUBTITLE
    elif ext in ("jpg", "jpeg", "png"):
        return enums.FileType.IMAGE
    return enums.FileType.OTHER


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
    def get_torrents(cls) -> models.ObjectSet[models.Addition]:
        return models.ObjectSet([cls.format_addition(torrent) for torrent in cls.client().get_torrents()])

    @staticmethod
    def format_addition(torrent: Torrent) -> models.Addition:
        return models.Addition(
            id=torrent.id,
            state=enums.State.DOWNLOADING,
            name=torrent.name,
            progress=torrent.progress,
            files=[
                # TODO: These still have the root folder
                models.File(
                    name=f.name,
                    file_type=get_file_extension(f.name),
                )
                for f in torrent.files()
            ],
        )


class FileSystem:
    @classmethod
    def get_files(cls) -> models.ObjectSet[models.Addition]:
        res = []
        for addition in os.listdir(settings.INCOMING_FOLDER):
            if addition in (".DS_Store",):
                continue
            addition_path = os.path.join(settings.INCOMING_FOLDER, addition)
            # Add single file cases
            if os.path.isfile(addition_path):
                # TODO: set a reliable ID
                res.append(
                    models.Addition(
                        id=addition,
                        state=enums.State.COMPLETED,
                        name=addition,
                        progress=1.0,
                        files=[cls.format_file(addition)],
                    )
                )
                continue
            # Add multi-file cases
            for root, _, files in os.walk(addition_path):
                addition_files = []
                for f in files:
                    file_name = os.path.relpath(os.path.join(root, f), start=addition_path)
                    addition_files.append(cls.format_file(file_name))
                res.append(
                    models.Addition(
                        id=addition,
                        state=enums.State.COMPLETED,
                        name=addition,
                        progress=1.0,
                        files=addition_files,
                    )
                )
        return models.ObjectSet(res)

    @staticmethod
    def format_file(file: str) -> models.File:
        return models.File(
            name=file,
            file_type=get_file_extension(file),
        )
