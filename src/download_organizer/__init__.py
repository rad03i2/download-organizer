"""Download Organizer: safe, local-first Downloads cleanup."""

from .core import Move, apply_plan, build_plan, category_for, undo

__all__ = ["Move", "apply_plan", "build_plan", "category_for", "undo"]
__version__ = "1.0.0"
