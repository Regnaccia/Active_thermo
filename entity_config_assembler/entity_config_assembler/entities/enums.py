from __future__ import annotations

from typing import Literal

Provider = Literal["config", "mqtt", "runtime", "derived"]
Role = Literal["input", "internal", "output"]
Domain = Literal[
    "sensor",
    "binary_sensor",
    "switch",
    "button",
    "select",
    "number",
    "text",
    "input_boolean",
    "input_button",
    "input_number",
    "input_select",
    "input_text",
]
NamingMode = Literal["keep_local_id", "prefix_parent"]
DERIVED_ALLOWED_DOMAINS = {"sensor", "binary_sensor"}
