from __future__ import annotations

from pathlib import Path

from entity_config_assembler.assembler.instance_assembler import InstanceAssembler
from entity_config_assembler.assembler.system_assembler import SystemAssembler
from entity_config_assembler.entities.assembly import (
    AssembledConfiguration,
    BuiltEntity,
    BuiltInstance,
    BuiltInstanceInfo,
    BuiltSystemInfo,
    NamingPolicy,
)
from entity_config_assembler.normalizers.entity_naming_policy import EntityNamingPolicy
from entity_config_assembler.utils.logging import indent, log


class ConfigurationAssembler:
    def __init__(
        self,
        *,
        base_path: Path,
        system_file: str,
        naming_policy: NamingPolicy | None = None,
        log_mode=None,
    ) -> None:
        self.base_path = Path(base_path)
        self.system_file = system_file
        self.naming_policy = naming_policy or NamingPolicy()
        self.log_mode = log_mode

    def assemble(self) -> AssembledConfiguration:
        log(self.log_mode, indent("⚙️ Assembling configuration", 0), level=0)
        system = SystemAssembler(
            base_path=self.base_path,
            system_file=self.system_file,
            log_mode=self.log_mode,
        ).assemble()

        initialized_instances = [instance for instance in system.instances if instance.initialize]
        instance_assemblies = [
            InstanceAssembler(
                base_path=self.base_path,
                instance=instance,
                log_mode=self.log_mode,
            ).assemble()
            for instance in initialized_instances
        ]

        naming = EntityNamingPolicy(self.naming_policy)
        entity_index = {
            entity.full_id: entity
            for instance in instance_assemblies
            for entity in instance.entities.iter_entities()
        }

        built_entities: list[BuiltEntity] = []
        built_instances: list[BuiltInstance] = []

        for instance in instance_assemblies:
            instance_exported_ids: list[str] = []
            for entity in instance.entities.iter_entities():
                exported_id = naming.exported_id_for(entity)
                resolved_dependencies = self._resolve_dependencies(entity_index=entity_index, entity=entity)
                built_entities.append(
                    BuiltEntity(
                        id=entity.id,
                        full_id=entity.full_id,
                        exported_id=exported_id,
                        name=entity.name,
                        parent=entity.parent,
                        domain=entity.domain,
                        provider=entity.provider,
                        role=entity.role,
                        expose=entity.expose,
                        source=entity.source,
                        dependencies=resolved_dependencies,
                        raw_dependencies=list(entity.dependencies),
                        evaluation=entity.evaluation if isinstance(entity.evaluation, dict) else entity.evaluation,
                    )
                )
                instance_exported_ids.append(exported_id)

            built_instances.append(
                BuiltInstance(
                    id=instance.id,
                    name=instance.name,
                    type=instance.type,
                    info=BuiltInstanceInfo(
                        router=instance.router_path,
                        entities=instance_exported_ids,
                        entities_count=len(instance_exported_ids),
                    ),
                )
            )

        return AssembledConfiguration(
            system=BuiltSystemInfo(
                name=system.name,
                instances=[instance.id for instance in instance_assemblies],
                instances_count=len(instance_assemblies),
            ),
            mqtt=system.mqtt,
            instances=built_instances,
            entities=built_entities,
            naming_policy=self.naming_policy,
        )

    @staticmethod
    def _resolve_dependencies(*, entity_index: dict[str, object], entity: object) -> list[str]:
        resolved: list[str] = []
        for dependency in getattr(entity, "dependencies", []):
            full_id = ConfigurationAssembler._resolve_dependency_full_id(
                dependency=dependency,
                parent=getattr(entity, "parent"),
            )
            if full_id not in entity_index:
                raise ValueError(
                    f"Entity '{getattr(entity, 'full_id')}' references missing dependency '{dependency}' "
                    f"(resolved as '{full_id}')."
                )
            resolved.append(full_id)
        return resolved

    @staticmethod
    def _resolve_dependency_full_id(*, dependency: str, parent: str) -> str:
        ref = dependency.strip()
        parts = ref.split(".")
        if len(parts) == 1:
            return f"{parent}.{parts[0]}"
        if len(parts) == 2:
            instance_id, local_id = parts
            if not instance_id or not local_id:
                raise ValueError(f"Invalid dependency reference '{dependency}'.")
            return f"{instance_id}.{local_id}"
        raise ValueError(
            f"Invalid dependency reference '{dependency}'. Supported formats are 'local_id' or 'instance_id.local_id'."
        )
