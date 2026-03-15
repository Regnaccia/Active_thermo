from __future__ import annotations

from collections import Counter, defaultdict

from pydantic import computed_field, model_validator

from entity_config_assembler.entities.enums import Domain, NamingMode, Provider, Role
from entity_config_assembler.entities.manifest import InstanceEntityManifest
from entity_config_assembler.entities.source import SourceConfig
from entity_config_assembler.entities.strict import StrictModel
from entity_config_assembler.entities.system import MqttConfig, RouterConfig


class NamingPolicy(StrictModel):
    mode: NamingMode = "prefix_parent"
    separator: str = "_"


class InstanceAssembly(StrictModel):
    id: str
    name: str
    type: str
    router_path: str
    router: RouterConfig
    entities: InstanceEntityManifest

    @computed_field
    @property
    def initialized_entity_ids(self) -> list[str]:
        return [entity.id for entity in self.entities.iter_entities()]

    @computed_field
    @property
    def initialized_entity_count(self) -> int:
        return len(self.initialized_entity_ids)


class BuiltSystemInfo(StrictModel):
    name: str
    instances: list[str]
    instances_count: int


class BuiltInstanceInfo(StrictModel):
    router: str
    entities: list[str]
    entities_count: int


class BuiltInstance(StrictModel):
    id: str
    name: str
    type: str
    info: BuiltInstanceInfo


class BuiltEntity(StrictModel):
    id: str
    full_id: str
    exported_id: str
    name: str
    parent: str
    domain: Domain
    provider: Provider
    role: Role
    expose: bool
    source: SourceConfig | None = None
    dependencies: list[str]
    raw_dependencies: list[str] = []
    evaluation: dict | None = None


class AssembledConfiguration(StrictModel):
    system: BuiltSystemInfo
    mqtt: MqttConfig
    instances: list[BuiltInstance]
    entities: list[BuiltEntity]
    naming_policy: NamingPolicy

    @model_validator(mode="after")
    def validate_global_uniqueness(self) -> "AssembledConfiguration":
        full_ids = [entity.full_id for entity in self.entities]
        duplicate_full_ids = sorted([key for key, count in Counter(full_ids).items() if count > 1])
        if duplicate_full_ids:
            raise ValueError(f"Duplicate full entity ids detected: {duplicate_full_ids}")

        exposed = [entity.exported_id for entity in self.entities if entity.expose]
        duplicate_exported_ids = sorted([key for key, count in Counter(exposed).items() if count > 1])
        if duplicate_exported_ids:
            owners: dict[str, list[str]] = defaultdict(list)
            for entity in self.entities:
                if entity.expose and entity.exported_id in duplicate_exported_ids:
                    owners[entity.exported_id].append(entity.full_id)
            details = {key: owners[key] for key in duplicate_exported_ids}
            raise ValueError(f"Duplicate exported entity ids detected: {details}")
        return self
