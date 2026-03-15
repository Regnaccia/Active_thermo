# entity_config_assembler

`entity_config_assembler` è il modulo 1 della nuova architettura. Il suo perimetro è intenzionalmente ristretto:

- caricare i file YAML
- validare la struttura con Pydantic
- assemblare le istanze inizializzate
- applicare la naming policy agli `exported_id`
- risolvere e normalizzare le dipendenze in `full_id`
- produrre un unico `AssembledConfiguration`

Non fa:

- registry building
- dependency graph runtime
- evaluation engine
- MQTT transport runtime

## Motivazione del refactoring finale

Nel repo precedente il modulo era ancora nominato in funzione di ActiveThermo e aveva due criticità principali:

1. il controllo di unicità globale controllava i `full_id` ma riportava un errore riferito agli `exported_id`
2. le `dependencies` restavano in forma raw senza una vera risoluzione canonica

Questa versione chiude il modulo come componente generico e riusabile, pronto da passare a un futuro modulo `registry_builder`.

## Regole congelate

### 1. Namespace delle istanze

Ogni `instance_id` definisce un namespace globale unico.

- `instance_id` duplicati: **non ammessi**
- `full_id = "{instance_id}.{local_id}"`

Questo elimina a monte collisioni strutturali nel sistema assemblato.

### 2. ID delle entità

Nei file di entità l'id è sempre **locale alla propria istanza**.

Esempi validi:

- `zone_01.temp_raw`
- `zone_02.temp_raw`
- `common.common_sensor_a`

Quindi due zone possono condividere lo stesso file sensori con `id: temp_raw`, perché il namespace viene fornito da `parent` durante l'assembly.

### 3. Exported ID

L'`exported_id` è derivato dalla naming policy.

Policy supportate:

- `prefix_parent` → consigliata
- `keep_local_id` → ammessa ma più fragile

Con `prefix_parent`:

- `zone_01.temp_raw` → `zone_01_temp_raw`
- `zone_02.temp_raw` → `zone_02_temp_raw`

### 4. Dependencies

Formati ammessi nei manifest:

- `temp_raw` → riferimento locale alla stessa istanza
- `common.common_sensor_a` → riferimento assoluto
- `zone_02.temp_raw` → riferimento assoluto cross-instance

Formato **non ammesso**:

- stringhe con più di un punto, per esempio `a.b.c`

Output del modulo:

- tutte le `dependencies` vengono normalizzate in `full_id`

Esempio:

- dentro `zone_01`, `temp_raw` diventa `zone_01.temp_raw`

### 5. Primitive vs derived

Le entità `derived` sono ammesse solo per:

- `sensor`
- `binary_sensor`

Regole:

- `derived` richiede almeno una dependency
- `derived` richiede `evaluation`
- `derived` non può avere `source`
- `mqtt` richiede `source.topic`
- i provider diversi da `mqtt` non possono definire `source`

## Output

L'output finale è un `AssembledConfiguration` con:

- `system`
- `mqtt`
- `instances`
- `entities`
- `naming_policy`

Ogni `BuiltEntity` contiene sia:

- `raw_dependencies` → la forma dichiarata nei file YAML
- `dependencies` → la forma canonica risolta in `full_id`

## Struttura del pacchetto

```text
entity_config_assembler/
  assembler/
    configuration_assembler.py
    instance_assembler.py
    system_assembler.py
    validators.py
  entities/
  loaders/
  normalizers/
  utils/
  tests/
main.py
```

## Uso CLI

```bash
python main.py \
  --base-path . \
  --system-file config/00_system/00_system.yaml \
  --naming-mode prefix_parent \
  --format json
```

## Confine architetturale finale

Pipeline completa prevista:

1. `entity_config_assembler`
2. `registry_builder`
3. runtime / engine
4. MQTT / transport

Questa separazione consente di riusare modulo 1 anche per applicazioni future diverse da ActiveThermo, per esempio una futura runtime `PassiveThermo`.
