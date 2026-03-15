from __future__ import annotations

from collections import Counter

from pydantic import Field, model_validator

from entity_config_assembler.entities.domain_entities import (
    BinarySensorEntity,
    ButtonEntity,
    InputBooleanEntity,
    InputButtonEntity,
    InputNumberEntity,
    InputSelectEntity,
    InputTextEntity,
    NumberEntity,
    SelectEntity,
    SensorEntity,
    SwitchEntity,
    TextEntity,
)
from entity_config_assembler.entities.strict import StrictModel


class InstanceEntityManifest(StrictModel):
    sensor: list[SensorEntity] = Field(default_factory=list)
    binary_sensor: list[BinarySensorEntity] = Field(default_factory=list)
    switch: list[SwitchEntity] = Field(default_factory=list)
    button: list[ButtonEntity] = Field(default_factory=list)
    select: list[SelectEntity] = Field(default_factory=list)
    number: list[NumberEntity] = Field(default_factory=list)
    text: list[TextEntity] = Field(default_factory=list)
    input_boolean: list[InputBooleanEntity] = Field(default_factory=list)
    input_button: list[InputButtonEntity] = Field(default_factory=list)
    input_number: list[InputNumberEntity] = Field(default_factory=list)
    input_select: list[InputSelectEntity] = Field(default_factory=list)
    input_text: list[InputTextEntity] = Field(default_factory=list)

    def iter_entities(self) -> list:
        return [
            *self.sensor,
            *self.binary_sensor,
            *self.switch,
            *self.button,
            *self.select,
            *self.number,
            *self.text,
            *self.input_boolean,
            *self.input_button,
            *self.input_number,
            *self.input_select,
            *self.input_text,
        ]

    @model_validator(mode="after")
    def validate_duplicate_ids(self) -> "InstanceEntityManifest":
        ids = [entity.id for entity in self.iter_entities()]
        full_ids = [entity.full_id for entity in self.iter_entities()]
        duplicate_ids = sorted([key for key, count in Counter(ids).items() if count > 1])
        duplicate_full_ids = sorted([key for key, count in Counter(full_ids).items() if count > 1])
        if duplicate_ids:
            raise ValueError(f"Duplicate local entity ids detected inside instance manifest: {duplicate_ids}")
        if duplicate_full_ids:
            raise ValueError(f"Duplicate full entity ids detected inside instance manifest: {duplicate_full_ids}")
        return self
