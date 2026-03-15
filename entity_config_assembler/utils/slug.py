from __future__ import annotations

import re


def slugify(value: str, *, separator: str = "_") -> str:
    text = value.strip().lower()
    text = re.sub(r"[^a-z0-9]+", separator, text)
    text = re.sub(rf"{re.escape(separator)}+", separator, text)
    return text.strip(separator)
