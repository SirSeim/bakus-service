from addition import models
from addition.clients import FileSystem


def test_rename_and_move_movie_single_file(incoming_folder, plex_folder):
    old_name = "test.mkv"
    new_title = "Final (year)"
    new_name = f"{new_title}.mkv"
    file = models.RenameFile(current_name=old_name, new_name=new_name)
    (incoming_folder / old_name).write_text("foo bar")

    FileSystem.rename_and_move_movie(old_name, new_title, [file])

    assert not (incoming_folder / old_name).exists(), "old file should no longer exist"

    new_file = plex_folder / FileSystem.MOVIES_FOLDER / new_title / new_name
    assert new_file.exists()
    assert new_file.read_text() == "foo bar"


def test_rename_and_move_movie_multiple_files(incoming_folder, plex_folder):
    old_name = "test_dir"
    new_title = "Final (year)"
    files = [
        # common patterns
        models.RenameFile(current_name="movie.mp4", new_name=f"{new_title}.mp4"),
        models.RenameFile(current_name="other.srt", new_name=f"{new_title}.en.srt"),
        models.RenameFile(current_name="spanish.srt", new_name=f"{new_title}.es.srt"),
        # allow extension changes
        models.RenameFile(current_name="sample.mp4", new_name="sample.mkv"),
        # move nested files
        models.RenameFile(current_name="videos/trailer.mp4", new_name="trailer.mp4"),
    ]

    for file in files:
        old_file = incoming_folder / old_name / file.current_name
        old_file.parent.mkdir(parents=True, exist_ok=True)
        old_file.write_text("foo bar")

    FileSystem.rename_and_move_movie(old_name, new_title, files)

    assert not (incoming_folder / old_name).exists(), "old folder should no longer exist"
    for file in files:
        new_file = plex_folder / FileSystem.MOVIES_FOLDER / new_title / file.new_name
        assert new_file.exists()
        assert new_file.read_text() == "foo bar"


def test_rename_and_move_movie_left_over_files(incoming_folder, plex_folder):
    old_name = "test_dir"
    new_title = "Final (year)"
    file_to_move = models.RenameFile(current_name="movie.mp4", new_name=f"{new_title}.mp4")
    file_to_leave = incoming_folder / old_name / "info.txt"
    file_to_leave.parent.mkdir()

    (incoming_folder / old_name / file_to_move.current_name).write_text("foo")
    file_to_leave.write_text("bar")

    FileSystem.rename_and_move_movie(old_name, new_title, [file_to_move])

    assert file_to_leave.exists()
    assert file_to_leave.read_text() == "bar"
    new_file = plex_folder / FileSystem.MOVIES_FOLDER / new_title / file_to_move.new_name
    assert new_file.exists()
    assert new_file.read_text() == "foo"


def test_rename_and_move_tv_season_single_file(incoming_folder, plex_folder):
    old_name = "test.mkv"
    new_title = "Final (year)"
    new_name = f"{new_title}.mkv"
    file = models.RenameFile(current_name=old_name, new_name=new_name)
    (incoming_folder / old_name).write_text("foo bar")

    FileSystem.rename_and_move_tv_season(old_name, new_title, 1, [file])

    assert not (incoming_folder / old_name).exists(), "old file should no longer exist"

    new_file = plex_folder / FileSystem.TV_SHOWS_FOLDER / new_title / "Season 01" / new_name
    assert new_file.exists()
    assert new_file.read_text() == "foo bar"


def test_rename_and_move_tv_season_multiple_files(incoming_folder, plex_folder):
    old_name = "test_dir"
    new_title = "Final (year)"
    files = [
        # common patterns
        models.RenameFile(current_name="movie.mp4", new_name=f"{new_title}.mp4"),
        models.RenameFile(current_name="other.srt", new_name=f"{new_title}.en.srt"),
        models.RenameFile(current_name="spanish.srt", new_name=f"{new_title}.es.srt"),
        # allow extension changes
        models.RenameFile(current_name="sample.mp4", new_name="sample.mkv"),
        # move nested files
        models.RenameFile(current_name="videos/trailer.mp4", new_name="trailer.mp4"),
    ]

    for file in files:
        old_file = incoming_folder / old_name / file.current_name
        old_file.parent.mkdir(parents=True, exist_ok=True)
        old_file.write_text("foo bar")

    FileSystem.rename_and_move_tv_season(old_name, new_title, 1, files)

    assert not (incoming_folder / old_name).exists(), "old folder should no longer exist"
    for file in files:
        new_file = plex_folder / FileSystem.TV_SHOWS_FOLDER / new_title / "Season 01" / file.new_name
        assert new_file.exists()
        assert new_file.read_text() == "foo bar"


def test_rename_and_move_tv_season_left_over_files(incoming_folder, plex_folder):
    old_name = "test_dir"
    new_title = "Final (year)"
    file_to_move = models.RenameFile(current_name="movie.mp4", new_name=f"{new_title}.mp4")
    file_to_leave = incoming_folder / old_name / "info.txt"
    file_to_leave.parent.mkdir()

    (incoming_folder / old_name / file_to_move.current_name).write_text("foo")
    file_to_leave.write_text("bar")

    FileSystem.rename_and_move_tv_season(old_name, new_title, 1, [file_to_move])

    assert file_to_leave.exists()
    assert file_to_leave.read_text() == "bar"
    new_file = plex_folder / FileSystem.TV_SHOWS_FOLDER / new_title / "Season 01" / file_to_move.new_name
    assert new_file.exists()
    assert new_file.read_text() == "foo"


def test_rename_and_move_tv_season_season_zero(incoming_folder, plex_folder):
    old_name = "test.mkv"
    new_title = "Final (year)"
    new_name = f"{new_title}.mkv"
    file = models.RenameFile(current_name=old_name, new_name=new_name)
    (incoming_folder / old_name).write_text("foo bar")

    FileSystem.rename_and_move_tv_season(old_name, new_title, 0, [file])

    assert not (incoming_folder / old_name).exists(), "old file should no longer exist"

    new_file = plex_folder / FileSystem.TV_SHOWS_FOLDER / new_title / "Season 00" / new_name
    assert new_file.exists()
    assert new_file.read_text() == "foo bar"


def test_rename_and_move_tv_season_season_already_exists_single_file(incoming_folder, plex_folder):
    old_name = "test.mkv"
    new_title = "Final (year)"
    new_name = f"{new_title}.mkv"
    file = models.RenameFile(current_name=old_name, new_name=new_name)
    (incoming_folder / old_name).write_text("foo bar")

    season_folder = plex_folder / FileSystem.TV_SHOWS_FOLDER / new_title / "Season 01"
    season_folder.mkdir(parents=True)
    (season_folder / "ep1.mkv").write_text("existing episode")

    FileSystem.rename_and_move_tv_season(old_name, new_title, 1, [file])

    assert not (incoming_folder / old_name).exists(), "old file should no longer exist"

    new_file = plex_folder / FileSystem.TV_SHOWS_FOLDER / new_title / "Season 01" / new_name
    assert new_file.exists()
    assert new_file.read_text() == "foo bar"


def test_rename_and_move_tv_season_season_already_exists_multiple_files(incoming_folder, plex_folder):
    old_name = "test_dir"
    new_title = "Final (year)"
    files = [
        # common patterns
        models.RenameFile(current_name="movie.mp4", new_name=f"{new_title}.mp4"),
        models.RenameFile(current_name="other.srt", new_name=f"{new_title}.en.srt"),
        models.RenameFile(current_name="spanish.srt", new_name=f"{new_title}.es.srt"),
        # allow extension changes
        models.RenameFile(current_name="sample.mp4", new_name="sample.mkv"),
        # move nested files
        models.RenameFile(current_name="videos/trailer.mp4", new_name="trailer.mp4"),
    ]

    for file in files:
        old_file = incoming_folder / old_name / file.current_name
        old_file.parent.mkdir(parents=True, exist_ok=True)
        old_file.write_text("foo bar")

    season_folder = plex_folder / FileSystem.TV_SHOWS_FOLDER / new_title / "Season 01"
    season_folder.mkdir(parents=True)

    FileSystem.rename_and_move_tv_season(old_name, new_title, 1, files)

    assert not (incoming_folder / old_name).exists(), "old folder should no longer exist"
    for file in files:
        new_file = season_folder / file.new_name
        assert new_file.exists()
        assert new_file.read_text() == "foo bar"
