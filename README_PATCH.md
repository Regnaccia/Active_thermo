# ActiveThermo evaluation patch

Files included:
- `entity_config_assembler/entities/evaluation.py` (new)
- `entity_config_assembler/entities/base.py`
- `entity_config_assembler/entities/assembly.py`
- `entity_config_assembler/assembler/configuration_assembler.py`
- `entity_config_assembler/entities/__init__.py`

## Supported YAML

Complex case:
```yaml
evaluation:
  kind: function
  engine: active_thermo
  function: temp_validator
  args:
    min_value: -20
    max_value: 60
```

Simple case:
```yaml
evaluation:
  kind: greater_than
  threshold: 20
```

Normalization:
- If `engine` is omitted, validation resolves it to `base`.
- Simple kinds are validated only against the `base` engine.
- `kind: function` is validated against the selected engine catalog.
