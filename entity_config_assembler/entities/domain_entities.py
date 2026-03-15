# entity_config_assembler/entity_config_assembler/entities/domain_entities.py

from __future__ import annotations
from pydantic import Field, AliasChoices
from entity_config_assembler.entities.base import BaseEntity


class SensorEntity(BaseEntity):
    @property
    def domain(self) -> str:
        return "sensor"


class BinarySensorEntity(BaseEntity):
    @property
    def domain(self) -> str:
        return "binary_sensor"


class SwitchEntity(BaseEntity):
    @property
    def domain(self) -> str:
        return "switch"


class ButtonEntity(BaseEntity):
    @property
    def domain(self) -> str:
        return "button"


class SelectEntity(BaseEntity):
    options: list[str] | None = None
    initial: str | None = None

    @property
    def domain(self) -> str:
        return "select"


class NumberEntity(BaseEntity):
    min_value: float | None = Field(default=None, validation_alias=AliasChoices("min_value", "min"))
    max_value: float | None = Field(default=None, validation_alias=AliasChoices("max_value", "max"))
    step: float | None = None
    initial: float | None = None

    @property
    def domain(self) -> str:
        return "number"


class TextEntity(BaseEntity):
    initial: str | None = None

    @property
    def domain(self) -> str:
        return "text"


class InputBooleanEntity(BaseEntity):
    initial: bool | None = None

    @property
    def domain(self) -> str:
        return "input_boolean"


class InputButtonEntity(BaseEntity):
    @property
    def domain(self) -> str:
        return "input_button"


class InputNumberEntity(NumberEntity):
    @property
    def domain(self) -> str:
        return "input_number"


class InputSelectEntity(SelectEntity):
    @property
    def domain(self) -> str:
        return "input_select"


class InputTextEntity(TextEntity):
    @property
    def domain(self) -> str:
        return "input_text"