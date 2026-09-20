from __future__ import annotations

import hashlib
import json
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

CATEGORIES: dict[str, set[str]] = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".heic"},
    "Videos": {".mp4", ".mkv", ".mov", ".avi", ".webm", ".m4v"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".md"},
    "Spreadsheets": {".csv", ".xls", ".xlsx", ".ods"},
    "Presentations": {".ppt", ".pptx", ".odp"},
    "Archives": {".zip", ".7z", ".rar", ".tar", ".gz", ".bz2", ".xz"},
    "Installers": {".exe", ".msi", ".msix", ".dmg", ".pkg", ".deb", ".rpm"},
    "Code": {".py", ".js", ".ts", ".html", ".css", ".json", ".yaml", ".yml", ".xml", ".sql"},
}


@dataclass(frozen=True)
class Move:
    source: str
    destination: str
    category: str
    size: int
    sha256: str


def category_for(path: Path) -> str:
    suffix = path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if suffix in extensions:
            return category
    return "Other"


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_destination(destination: Path, reserved: set[Path]) -> Path:
    if destination not in reserved and not destination.exists():
        return destination
    stem, suffix = destination.stem, destination.suffix
    counter = 1
    while True:
        candidate = destination.with_name(f"{stem} ({counter}){suffix}")
        if candidate not in reserved and not candidate.exists():
            return candidate
        counter += 1


def iter_files(root: Path, *, recursive: bool = False, include_hidden: bool = False) -> Iterable[Path]:
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"Not a directory: {root}")
    iterator = root.rglob("*") if recursive else root.iterdir()
    for path in iterator:
        if not path.is_file() or path.is_symlink():
            continue
        relative = path.relative_to(root)
        if not include_hidden and any(part.startswith(".") for part in relative.parts):
            continue
        yield path


def build_plan(root: Path, *, recursive: bool = False, include_hidden: bool = False) -> list[Move]:
    root = root.expanduser().resolve()
    reserved: set[Path] = set()
    moves: list[Move] = []
    for source in sorted(iter_files(root, recursive=recursive, include_hidden=include_hidden)):
        # Never reorganize files already inside one of our category directories.
        relative = source.relative_to(root)
        if len(relative.parts) > 1 and relative.parts[0] in {*CATEGORIES, "Other"}:
            continue
        category = category_for(source)
        destination = _safe_destination(root / category / source.name, reserved)
        reserved.add(destination)
        moves.append(Move(str(source), str(destination), category, source.stat().st_size, sha256_file(source)))
    return moves


def apply_plan(moves: list[Move], manifest: Path) -> Path:
    completed: list[Move] = []
    try:
        for move in moves:
            source, destination = Path(move.source), Path(move.destination)
            if not source.is_file():
                raise FileNotFoundError(source)
            if sha256_file(source) != move.sha256:
                raise RuntimeError(f"File changed since preview: {source}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.exists():
                raise FileExistsError(destination)
            shutil.move(str(source), str(destination))
            completed.append(move)
    except Exception:
        for move in reversed(completed):
            source, destination = Path(move.source), Path(move.destination)
            if destination.exists() and not source.exists():
                source.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(destination), str(source))
        raise

    payload = {
        "version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "moves": [asdict(move) for move in completed],
    }
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return manifest


def undo(manifest: Path) -> int:
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    moves = [Move(**item) for item in payload.get("moves", [])]
    restored = 0
    for move in reversed(moves):
        source, destination = Path(move.source), Path(move.destination)
        if not destination.is_file():
            raise FileNotFoundError(f"Organized file is missing: {destination}")
        if source.exists():
            raise FileExistsError(f"Original path is occupied: {source}")
        if sha256_file(destination) != move.sha256:
            raise RuntimeError(f"Organized file changed; refusing undo: {destination}")
        source.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(destination), str(source))
        restored += 1
    return restored
