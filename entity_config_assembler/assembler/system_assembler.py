from __future__ import annotations

from pathlib import Path

from entity_config_assembler.assembler.validators import (
    validate_instances_package,
    validate_mqtt_config,
    validate_system_config,
)
from entity_config_assembler.entities.system import SystemAssembly
from entity_config_assembler.loaders.config_loaders import load_yaml_config
from entity_config_assembler.utils.logging import indent, log


class SystemAssembler:
    def __init__(self, *, base_path: Path, system_file: str, log_mode=None) -> None:
        self.base_path = Path(base_path)
        self.system_file = system_file
        self.log_mode = log_mode

    def assemble(self) -> SystemAssembly:
        log(self.log_mode, indent("⚙️ Assembling system", 1), level=1)
        raw_system = load_yaml_config(
            base_path=self.base_path,
            file_path=self.system_file,
            log_mode=self.log_mode,
            label="System configuration",
            level=1,
        )
        system = validate_system_config(raw_system, self.log_mode)

        raw_mqtt = load_yaml_config(
            base_path=self.base_path,
            file_path=system.mqtt_config,
            log_mode=self.log_mode,
            label="MQTT configuration",
            level=1,
        )
        mqtt = validate_mqtt_config(raw_mqtt, self.log_mode)

        raw_instances = load_yaml_config(
            base_path=self.base_path,
            file_path=system.instances_package,
            log_mode=self.log_mode,
            label="Instances package",
            level=1,
        )
        instances = validate_instances_package(raw_instances, self.log_mode)

        return SystemAssembly(name=system.system_name, mqtt=mqtt, instances=instances)
