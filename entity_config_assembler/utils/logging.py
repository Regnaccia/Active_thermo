from __future__ import annotations

from typing import Literal

LogMode = Literal["silent", "normal", "verbose"]


def indent(text: str, level: int) -> str:
    return f"{'  ' * max(level, 0)}{text}"


def log(log_mode: LogMode | None, message: str, *, level: int = 0) -> None:
    mode = log_mode or "normal"
    if mode == "silent":
        return
    if mode == "normal" and level > 0:
        return
    print(message)
