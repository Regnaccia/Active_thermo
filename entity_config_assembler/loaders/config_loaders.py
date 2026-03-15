from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from entity_config_assembler.utils.logging import log


def load_yaml_config(
    *,
    base_path: Path,
    file_path: str,
    log_mode=None,
    label: str | None = None,
    level: int = 0,
) -> Any:
    resolved = (Path(base_path) / file_path).resolve()
    if not resolved.is_file():
        raise FileNotFoundError(f"YAML file not found: {resolved}")

    if label:
        log(log_mode, f"{'  ' * level}📄 Loading {label}: {resolved}", level=level)

    with resolved.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)
