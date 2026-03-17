from __future__ import annotations

from typing import Any, Literal

from pydantic import ConfigDict, Field, model_validator

from entity_config_assembler.entities.strict import StrictModel


EVALUATION_CATALOG: dict[str, set[str]] = {
    "base": {
        "equals",
        "not_equals",
        "greater_than",
        "greater_or_equal",
        "less_than",
        "less_or_equal",
        "in_range",
        "and",
        "or",
        "not",
        "add",
        "subtract",
        "multiply",
        "divide",
        "average",
        "min",
        "max",
    },
    "active_thermo": {
        "temp_validator",
    },
    "passive_thermo": set(),
}


def _known_engines() -> list[str]:
    return sorted(EVALUATION_CATALOG.keys())


def _resolve_engine(engine: str | None) -> str:
    return (engine or "base").strip()


class SimpleEvaluation(StrictModel):
    model_config = ConfigDict(extra="allow", str_strip_whitespace=True)

    kind: str = Field(min_length=1)
    engine: str | None = None

    @model_validator(mode="after")
    def validate_simple_evaluation(self) -> "SimpleEvaluation":
        normalized_engine = _resolve_engine(self.engine)
        if normalized_engine != "base":
            raise ValueError(
                "Simple evaluation kinds are resolved only against engine='base'. "
                f"Received engine='{normalized_engine}'."
            )

        if self.kind == "function":
            raise ValueError("SimpleEvaluation cannot be used for kind='function'.")

        if self.kind not in EVALUATION_CATALOG["base"]:
            raise ValueError(
                f"Unknown base evaluation kind '{self.kind}'. "
                f"Available kinds: {sorted(EVALUATION_CATALOG['base'])}."
            )

        object.__setattr__(self, "engine", normalized_engine)
        return self


class FunctionEvaluation(StrictModel):
    kind: Literal["function"] = "function"
    engine: str | None = None
    function: str = Field(min_length=1)
    args: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_function_evaluation(self) -> "FunctionEvaluation":
        normalized_engine = _resolve_engine(self.engine)

        if normalized_engine not in EVALUATION_CATALOG:
            raise ValueError(
                f"Unknown evaluation engine '{normalized_engine}'. "
                f"Available engines: {_known_engines()}."
            )

        if self.function not in EVALUATION_CATALOG[normalized_engine]:
            raise ValueError(
                f"Unknown function '{normalized_engine}/{self.function}'. "
                f"Available functions for engine '{normalized_engine}': "
                f"{sorted(EVALUATION_CATALOG[normalized_engine])}."
            )

        object.__setattr__(self, "engine", normalized_engine)
        return self


EvaluationConfig = SimpleEvaluation | FunctionEvaluation


def parse_evaluation_config(value: Any) -> EvaluationConfig | None:
    if value is None:
        return None

    if isinstance(value, (SimpleEvaluation, FunctionEvaluation)):
        return value

    if not isinstance(value, dict):
        raise TypeError("Evaluation must be a mapping.")

    kind = str(value.get("kind", "")).strip()
    if not kind:
        raise ValueError("Evaluation requires a non-empty 'kind' field.")

    if kind == "function":
        return FunctionEvaluation.model_validate(value)

    return SimpleEvaluation.model_validate(value)
