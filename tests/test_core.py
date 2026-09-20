from pathlib import Path

import pytest

from download_organizer.core import apply_plan, build_plan, category_for, undo


def test_categories_are_case_insensitive(tmp_path: Path):
    assert category_for(tmp_path / "photo.JPG") == "Images"
    assert category_for(tmp_path / "unknown.xyz") == "Other"


def test_plan_apply_and_undo(tmp_path: Path):
    source = tmp_path / "report.pdf"
    source.write_bytes(b"important")
    moves = build_plan(tmp_path)
    assert len(moves) == 1
    assert Path(moves[0].destination) == tmp_path / "Documents" / "report.pdf"
    manifest = tmp_path / "manifest.json"
    apply_plan(moves, manifest)
    assert not source.exists()
    assert (tmp_path / "Documents" / "report.pdf").read_bytes() == b"important"
    assert undo(manifest) == 1
    assert source.read_bytes() == b"important"


def test_collision_is_resolved_without_overwrite(tmp_path: Path):
    (tmp_path / "Images").mkdir()
    (tmp_path / "Images" / "cat.jpg").write_bytes(b"old")
    (tmp_path / "cat.jpg").write_bytes(b"new")
    move = build_plan(tmp_path)[0]
    assert Path(move.destination).name == "cat (1).jpg"


def test_hidden_files_are_skipped_by_default(tmp_path: Path):
    (tmp_path / ".secret.txt").write_text("secret")
    assert build_plan(tmp_path) == []
    assert len(build_plan(tmp_path, include_hidden=True)) == 1


def test_existing_category_files_are_not_reorganized(tmp_path: Path):
    folder = tmp_path / "Documents"
    folder.mkdir()
    (folder / "a.pdf").write_bytes(b"x")
    assert build_plan(tmp_path, recursive=True) == []


def test_changed_file_is_refused(tmp_path: Path):
    source = tmp_path / "a.txt"
    source.write_text("one")
    plan = build_plan(tmp_path)
    source.write_text("two")
    with pytest.raises(RuntimeError, match="changed"):
        apply_plan(plan, tmp_path / "manifest.json")
    assert source.read_text() == "two"


def test_undo_refuses_modified_destination(tmp_path: Path):
    source = tmp_path / "a.txt"
    source.write_text("one")
    manifest = tmp_path / "manifest.json"
    apply_plan(build_plan(tmp_path), manifest)
    (tmp_path / "Documents" / "a.txt").write_text("modified")
    with pytest.raises(RuntimeError, match="changed"):
        undo(manifest)
