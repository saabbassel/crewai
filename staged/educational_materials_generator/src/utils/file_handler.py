"""File utilities for read/write and directory management."""
import json
from pathlib import Path
from typing import Any


def ensure_dir(path: str) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def read_json(path: str) -> Any:
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(obj: Any, path: str, indent: int = 2) -> None:
    p = Path(path)
    ensure_dir(p.parent.as_posix())
    with p.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=indent, ensure_ascii=False)


def write_markdown(content: str, path: str) -> None:
    p = Path(path)
    ensure_dir(p.parent.as_posix())
    with p.open("w", encoding="utf-8") as f:
        f.write(content)
