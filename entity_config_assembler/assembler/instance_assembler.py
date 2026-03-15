from __future__ import annotations

from pathlib import Path

from entity_config_assembler.assembler.validators import validate_instance_entity_manifest, validate_router_config
from entity_config_assembler.entities.assembly import InstanceAssembly
from entity_config_assembler.entities.system import PackageConfig
from entity_config_assembler.loaders.config_loaders import load_yaml_config
from entity_config_assembler.utils.logging import indent, log

SUPPORTED_DOMAINS = {
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
}


class InstanceAssembler:
    def __init__(self, *, base_path: Path, instance: PackageConfig, log_mode=None) -> None:
        self.base_path = Path(base_path)
        self.instance = instance
        self.log_mode = log_mode

    def assemble(self) -> InstanceAssembly:
        log(self.log_mode, indent(f"⚙️ Assembling instance '{self.instance.name}'", 1), level=1)
        raw_router = load_yaml_config(
            base_path=self.base_path,
            file_path=self.instance.router,
            log_mode=self.log_mode,
            label=f"Router for '{self.instance.id}'",
            level=2,
        )
        router = validate_router_config(raw_router, self.log_mode)

        aggregated: dict[str, list[dict]] = {domain: [] for domain in SUPPORTED_DOMAINS}
        for entity_file in router.entities:
            raw_manifest = load_yaml_config(
                base_path=self.base_path,
                file_path=entity_file,
                log_mode=self.log_mode,
                label=f"Entity manifest '{entity_file}'",
                level=3,
            )
            if not isinstance(raw_manifest, dict):
                raise ValueError(
                    f"Entity manifest '{entity_file}' for instance '{self.instance.id}' must contain a mapping."
                )
            for domain, values in raw_manifest.items():
                if values is None:
                    continue
                if domain not in aggregated:
                    raise ValueError(f"Unsupported entity domain '{domain}' in entity manifest '{entity_file}'.")
                if not isinstance(values, list):
                    raise ValueError(
                        f"Entity manifest '{entity_file}' domain '{domain}' must contain a list of entities."
                    )
                for item in values:
                    if not isinstance(item, dict):
                        raise ValueError(
                            f"Entity manifest '{entity_file}' domain '{domain}' must contain mapping items."
                        )
                    normalized = dict(item)
                    normalized["parent"] = self.instance.id
                    aggregated[domain].append(normalized)

        entities = validate_instance_entity_manifest(aggregated, self.log_mode)
        return InstanceAssembly(
            id=self.instance.id,
            name=self.instance.name,
            type=self.instance.type,
            router_path=self.instance.router,
            router=router,
            entities=entities,
        )
