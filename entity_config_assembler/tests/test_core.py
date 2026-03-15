from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from entity_config_assembler import ConfigurationAssembler, NamingPolicy


def _write_yaml(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def _build_basic_project(tmp_path: Path, *, naming_mode: str = "prefix_parent", extra_zone: bool = True) -> ConfigurationAssembler:
    _write_yaml(
        tmp_path / "config/00_system/00_system.yaml",
        {
            "system_name": "Casa Regna",
            "mqtt_config": "config/00_system/mqtt.yaml",
            "instances_package": "config/00_system/instances.yaml",
        },
    )
    _write_yaml(
        tmp_path / "config/00_system/mqtt.yaml",
        {"broker": "127.0.0.1", "port": 1883, "username": "u", "password": "p"},
    )

    instances = [
        {"id": "system", "name": "System", "type": "system", "router": "config/system_router.yaml"},
        {"id": "common", "name": "Common", "type": "common", "router": "config/common_router.yaml"},
        {"id": "zone_01", "name": "Zona 1", "type": "zone", "router": "config/zone_router.yaml"},
    ]
    if extra_zone:
        instances.append({"id": "zone_02", "name": "Zona 2", "type": "zone", "router": "config/zone_router.yaml"})
    _write_yaml(tmp_path / "config/00_system/instances.yaml", instances)

    _write_yaml(tmp_path / "config/system_router.yaml", {"entities": []})
    _write_yaml(tmp_path / "config/common_router.yaml", {"entities": ["config/common_entities.yaml"]})
    _write_yaml(tmp_path / "config/zone_router.yaml", {"entities": ["config/zone_entities.yaml"]})

    _write_yaml(
        tmp_path / "config/common_entities.yaml",
        {
            "sensor": [
                {
                    "id": "common_sensor_a",
                    "name": "Common Sensor A",
                    "provider": "mqtt",
                    "role": "input",
                    "source": {"topic": "thermo/common/a/state"},
                }
            ]
        },
    )
    _write_yaml(
        tmp_path / "config/zone_entities.yaml",
        {
            "sensor": [
                {
                    "id": "temp_raw",
                    "name": "Temp Raw",
                    "provider": "mqtt",
                    "role": "input",
                    "source": {"topic": "thermo/zone/temp_raw/state"},
                },
                {
                    "id": "temp_copy",
                    "name": "Temp Copy",
                    "provider": "derived",
                    "role": "internal",
                    "dependencies": ["temp_raw", "common.common_sensor_a"],
                    "evaluation": {"kind": "copy"},
                },
            ]
        },
    )

    return ConfigurationAssembler(
        base_path=tmp_path,
        system_file="config/00_system/00_system.yaml",
        naming_policy=NamingPolicy(mode=naming_mode),
        log_mode="silent",
    )


def test_prefix_parent_allows_shared_zone_manifest(tmp_path: Path) -> None:
    config = _build_basic_project(tmp_path).assemble()
    exported_ids = {entity.exported_id for entity in config.entities if entity.id == "temp_raw"}
    assert exported_ids == {"zone_01_temp_raw", "zone_02_temp_raw"}


def test_dependencies_are_resolved_to_full_ids(tmp_path: Path) -> None:
    config = _build_basic_project(tmp_path).assemble()
    temp_copy_zone_01 = next(entity for entity in config.entities if entity.full_id == "zone_01.temp_copy")
    assert temp_copy_zone_01.raw_dependencies == ["temp_raw", "common.common_sensor_a"]
    assert temp_copy_zone_01.dependencies == ["zone_01.temp_raw", "common.common_sensor_a"]


def test_keep_local_id_detects_exported_collisions(tmp_path: Path) -> None:
    assembler = _build_basic_project(tmp_path, naming_mode="keep_local_id")
    with pytest.raises(ValueError, match="Duplicate exported entity ids"):
        assembler.assemble()


def test_duplicate_instance_ids_are_rejected(tmp_path: Path) -> None:
    assembler = _build_basic_project(tmp_path)
    instances_path = tmp_path / "config/00_system/instances.yaml"
    payload = yaml.safe_load(instances_path.read_text(encoding="utf-8"))
    payload.append({"id": "zone_01", "name": "Dup", "type": "zone", "router": "config/zone_router.yaml"})
    _write_yaml(instances_path, payload)

    with pytest.raises(ValueError, match="Duplicate instance ids"):
        assembler.assemble()


def test_missing_dependency_is_rejected(tmp_path: Path) -> None:
    assembler = _build_basic_project(tmp_path, extra_zone=False)
    zone_entities = tmp_path / "config/zone_entities.yaml"
    payload = yaml.safe_load(zone_entities.read_text(encoding="utf-8"))
    payload["sensor"][1]["dependencies"] = ["missing_sensor"]
    _write_yaml(zone_entities, payload)

    with pytest.raises(ValueError, match="references missing dependency"):
        assembler.assemble()
