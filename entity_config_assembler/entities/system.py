from __future__ import annotations

from pydantic import Field, field_validator

from entity_config_assembler.entities.strict import StrictModel


class MqttConfig(StrictModel):
    broker: str = Field(min_length=1)
    port: int = Field(ge=1, le=65535)
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class SystemConfig(StrictModel):
    system_name: str = Field(min_length=1)
    mqtt_config: str = Field(min_length=1)
    instances_package: str = Field(min_length=1)


class PackageConfig(StrictModel):
    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    type: str = Field(min_length=1)
    router: str = Field(min_length=1)
    initialize: bool = True

    @field_validator("id")
    @classmethod
    def validate_instance_id(cls, value: str) -> str:
        if "." in value:
            raise ValueError("Instance id cannot contain '.'.")
        return value

    @field_validator("type")
    @classmethod
    def normalize_type(cls, value: str) -> str:
        return value.lower()


class RouterConfig(StrictModel):
    entities: list[str] = Field(default_factory=list)


class SystemAssembly(StrictModel):
    name: str
    mqtt: MqttConfig
    instances: list[PackageConfig]
