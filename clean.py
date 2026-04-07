"""Clean build artifacts and caches for a fresh rebuild."""

import shutil
from pathlib import Path

ROOT = Path(__file__).parent

DIRS_TO_DELETE = [
    ".venv",
    "dist",
    "build",
    "htmlcov",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".ipynb_checkpoints",
]

GLOB_PATTERNS = [
    "**/*.egg-info",
    "**/__pycache__",
    "**/.ipynb_checkpoints",
]


def _remove(path: Path) -> None:
    try:
        shutil.rmtree(path)
        print(f"Removed {path}")
    except PermissionError as e:
        print(f"Skipped {path} (in use: {e})")


def clean() -> None:
    for name in DIRS_TO_DELETE:
        path = ROOT / name
        if path.exists():
            _remove(path)

    for pattern in GLOB_PATTERNS:
        for path in ROOT.glob(pattern):
            if path.is_dir():
                _remove(path)


if __name__ == "__main__":
    clean()
