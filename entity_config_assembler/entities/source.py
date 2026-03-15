from __future__ import annotations

from pydantic import Field

from entity_config_assembler.entities.strict import StrictModel


class MqttSource(StrictModel):
    topic: str = Field(min_length=1)


SourceConfig = MqttSource
