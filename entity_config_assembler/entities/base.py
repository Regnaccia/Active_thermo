from __future__ import annotations

from typing import Any

from pydantic import Field, field_validator, model_validator

from entity_config_assembler.entities.enums import DERIVED_ALLOWED_DOMAINS, Provider, Role
from entity_config_assembler.entities.source import SourceConfig
from entity_config_assembler.entities.strict import StrictModel


class BaseEntity(StrictModel):
    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    parent: str = Field(min_length=1)
    provider: Provider
    role: Role
    expose: bool = True
    icon: str | None = None
    unit_of_measurement: str | None = None
    device_class: str | None = None
    entity_category: str | None = None
    enabled_by_default: bool = True
    source: SourceConfig | None = None
    dependencies: list[str] = Field(default_factory=list)
    evaluation: Any | None = None

    @field_validator("id", "parent")
    @classmethod
    def validate_no_dot_in_identifiers(cls, value: str) -> str:
        if "." in value:
            raise ValueError("Entity local id and parent cannot contain '.'.")
        return value

    @field_validator("dependencies")
    @classmethod
    def validate_dependencies_not_blank(cls, values: list[str]) -> list[str]:
        seen: set[str] = set()
        normalized: list[str] = []
        for value in values:
            item = value.strip()
            if not item:
                raise ValueError("Dependencies cannot contain empty values.")
            if item in seen:
                raise ValueError(f"Duplicate dependency '{item}' detected.")
            seen.add(item)
            normalized.append(item)
        return normalized

    @property
    def is_derived(self) -> bool:
        return self.provider == "derived"

    @property
    def full_id(self) -> str:
        return f"{self.parent}.{self.id}"

    @property
    def domain(self) -> str:
        raise NotImplementedError

    @model_validator(mode="after")
    def validate_entity_rules(self) -> "BaseEntity":
        has_deps = bool(self.dependencies)
        has_eval = self.evaluation is not None
        has_source = self.source is not None

        if self.provider == "derived":
            if self.domain not in DERIVED_ALLOWED_DOMAINS:
                raise ValueError(
                    f"Derived entities are allowed only for domains: {sorted(DERIVED_ALLOWED_DOMAINS)}."
                )
            if not has_deps:
                raise ValueError("Derived entity requires at least one dependency.")
            if not has_eval:
                raise ValueError("Derived entity requires an evaluation block.")
            if has_source:
                raise ValueError("Derived entity cannot define source.")
        else:
            if has_deps:
                raise ValueError("Primitive entity cannot define dependencies.")
            if has_eval:
                raise ValueError("Primitive entity cannot define evaluation.")
            if self.provider == "mqtt" and self.source is None:
                raise ValueError("MQTT entity requires source.topic.")
            if self.provider != "mqtt" and has_source:
                raise ValueError("Source is supported only for provider='mqtt'.")

        return self
