# README note - entity syntax update

Aggiornamento suggerito per il README o per la documentazione principale del repository:

## Evaluation syntax

Le entità `derived` supportano due forme di evaluation:

### Caso semplice built-in

```yaml
evaluation:
  kind: greater_than
  threshold: 20
```

Gli operatori semplici vengono risolti come appartenenti logicamente al motore `base`.

### Caso complesso con funzione di engine

```yaml
evaluation:
  kind: function
  engine: active_thermo
  function: temp_validator
  args:
    min_value: -20
    max_value: 60
```

Questa sintassi prepara il progetto a una architettura multi-engine, con almeno:

- `base`
- `active_thermo`
- `passive_thermo`

Il YAML non contiene codice eseguibile: contiene solo riferimenti a funzioni dichiarate nel catalogo interno dell'engine.
