from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from .core import apply_plan, build_plan, undo


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="download-organizer", description="Safely organize a Downloads folder by file type.")
    sub = p.add_subparsers(dest="command", required=True)
    organize = sub.add_parser("organize", help="Preview or apply an organization plan")
    organize.add_argument("folder", type=Path)
    organize.add_argument("--recursive", action="store_true")
    organize.add_argument("--include-hidden", action="store_true")
    organize.add_argument("--apply", action="store_true", help="Actually move files; default is preview only")
    organize.add_argument("--manifest", type=Path, help="Undo manifest path")
    organize.add_argument("--json", action="store_true", help="Print the plan as JSON")
    restore = sub.add_parser("undo", help="Undo a previously applied organization")
    restore.add_argument("manifest", type=Path)
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "undo":
            count = undo(args.manifest)
            print(f"Restored {count} file(s).")
            return 0
        moves = build_plan(args.folder, recursive=args.recursive, include_hidden=args.include_hidden)
        if args.json:
            print(json.dumps([asdict(m) for m in moves], indent=2, ensure_ascii=False))
        else:
            for move in moves:
                print(f"[{move.category}] {move.source} -> {move.destination}")
            print(f"Planned {len(moves)} move(s). {'Applying...' if args.apply else 'Preview only; no files changed.'}")
        if args.apply and moves:
            manifest = args.manifest or (Path(args.folder).expanduser().resolve() / ".download-organizer" / f"manifest-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json")
            apply_plan(moves, manifest)
            print(f"Manifest: {manifest}")
        return 0
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
