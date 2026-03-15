from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from entity_config_assembler.entities.assembly import NamingPolicy
from entity_config_assembler.entities.manifest import InstanceEntityManifest
from entity_config_assembler.entities.system import MqttConfig, PackageConfig, RouterConfig, SystemConfig
from entity_config_assembler.utils.logging import LogMode, indent, log


def _convert_validation_error(label: str, exc: ValidationError) -> ValueError:
    error = ValueError(f"{label} validation failed:\n{exc}")
    error.__cause__ = exc
    return error


def validate_system_config(raw: Any, log_mode: LogMode) -> SystemConfig:
    try:
        model = SystemConfig.model_validate(raw)
    except ValidationError as exc:
        raise _convert_validation_error("System configuration", exc)
    log(log_mode, indent("✅ System configuration validated successfully", 1), level=1)
    return model


def validate_mqtt_config(raw: Any, log_mode: LogMode) -> MqttConfig:
    try:
        model = MqttConfig.model_validate(raw)
    except ValidationError as exc:
        raise _convert_validation_error("MQTT configuration", exc)
    log(log_mode, indent("✅ MQTT configuration validated successfully", 1), level=1)
    return model


def validate_instances_package(raw: Any, log_mode: LogMode) -> list[PackageConfig]:
    if not isinstance(raw, list):
        raise ValueError("Instances package must be a list of instance definitions.")
    try:
        models = [PackageConfig.model_validate(item) for item in raw]
    except ValidationError as exc:
        raise _convert_validation_error("Instances package", exc)

    if not models:
        raise ValueError("Instances package is empty.")

    ids = [item.id for item in models]
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        raise ValueError(f"Duplicate instance ids detected: {duplicates}")

    initialized = [item for item in models if item.initialize]
    if not initialized:
        raise ValueError("No initialized instances found in instances package.")

    type_counts: dict[str, int] = {}
    for item in initialized:
        type_counts[item.type] = type_counts.get(item.type, 0) + 1

    for required_singleton in ("system", "common"):
        count = type_counts.get(required_singleton, 0)
        if count == 0:
            raise ValueError(f"No initialized '{required_singleton}' instance found.")
        if count > 1:
            raise ValueError(f"More than one initialized '{required_singleton}' instance found.")

    log(log_mode, indent("✅ Instances package validated successfully", 1), level=1)
    return models


def validate_router_config(raw: Any, log_mode: LogMode) -> RouterConfig:
    try:
        model = RouterConfig.model_validate(raw)
    except ValidationError as exc:
        raise _convert_validation_error("Router configuration", exc)
    log(log_mode, indent("✅ Router configuration validated successfully", 2), level=2)
    return model


def validate_instance_entity_manifest(raw: Any, log_mode: LogMode) -> InstanceEntityManifest:
    try:
        model = InstanceEntityManifest.model_validate(raw)
    except ValidationError as exc:
        raise _convert_validation_error("Instance entity manifest", exc)
    log(log_mode, indent("✅ Instance entity manifest validated successfully", 3), level=3)
    return model


def validate_naming_policy(raw: Any, log_mode: LogMode) -> NamingPolicy:
    try:
        model = NamingPolicy.model_validate(raw)
    except ValidationError as exc:
        raise _convert_validation_error("Naming policy", exc)
    log(log_mode, indent("✅ Naming policy validated successfully", 1), level=1)
    return model
