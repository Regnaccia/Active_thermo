from __future__ import annotations

from entity_config_assembler.entities.assembly import NamingPolicy
from entity_config_assembler.entities.base import BaseEntity
from entity_config_assembler.utils.slug import slugify


class EntityNamingPolicy:
    def __init__(self, policy: NamingPolicy) -> None:
        self.policy = policy

    def exported_id_for(self, entity: BaseEntity) -> str:
        local_id = slugify(entity.id, separator=self.policy.separator)
        parent_id = slugify(entity.parent, separator=self.policy.separator)
        if self.policy.mode == "keep_local_id":
            return local_id
        if self.policy.mode == "prefix_parent":
            return f"{parent_id}{self.policy.separator}{local_id}"
        raise ValueError(f"Unsupported naming mode: {self.policy.mode}")
