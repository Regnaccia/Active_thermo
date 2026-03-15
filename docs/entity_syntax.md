# Entity Syntax

Questo documento descrive in modo esaustivo la sintassi delle entità nei file YAML di ActiveThermo.

L'obiettivo di questa sintassi è permettere una definizione:

- leggibile
- validabile
- estendibile
- indipendente dal runtime

Il file entity manifest descrive **quali entità esistono** in una specifica istanza e **come sono collegate** tra loro.

---

# 1. Struttura generale di un entity manifest

Un file manifest è un mapping YAML in cui ogni chiave di primo livello rappresenta un **domain**.

Esempio:

```yaml
sensor:
  - id: temp_raw
    name: Temperature Raw
    provider: mqtt
    role: input

binary_sensor:
  - id: cool_ready
    name: Cool Ready
    provider: derived
    role: state
    dependencies:
      - general_cool_enable
      - master_ac_cool_capable
```

Ogni lista sotto un domain contiene una o più entità di quel tipo.

---

# 2. Concetti base

Ogni entità è definita da tre livelli logici di identificazione:

- **domain**: tipo dell'entità, ad esempio `sensor` o `switch`
- **local id**: identificatore locale all'interno dell'istanza, ad esempio `temp_raw`
- **instance namespace**: namespace dell'istanza, ad esempio `zone_01`

Dal punto di vista logico:

- `temp_raw` è l'id locale
- `zone_01.temp_raw` è il riferimento pieno namespaced
- `zone_01_temp_raw` può essere il canonical/exported id finale, in base alla naming policy

---

# 3. Campi comuni

Questi campi costituiscono il nucleo comune della sintassi.

## 3.1 Campi obbligatori minimi

| Campo | Tipo | Descrizione |
|---|---|---|
| `id` | string | Identificatore locale univoco nell'istanza |
| `name` | string | Nome leggibile dell'entità |
| `provider` | string | Origine logica dell'entità |
| `role` | string | Ruolo logico dell'entità |

Esempio minimo:

```yaml
sensor:
  - id: temp_raw
    name: Temperature Raw
    provider: mqtt
    role: input
```

## 3.2 Campi opzionali comuni

| Campo | Tipo | Descrizione |
|---|---|---|
| `dependencies` | list[string] | Lista delle dipendenze logiche |
| `source` | object | Configurazione della sorgente dati |
| `evaluation` | object | Configurazione della logica derivata |
| `expose` | bool | Indica se l'entità deve essere esposta verso layer esterni |

Nota: la disponibilità effettiva di alcuni campi dipende dal domain e dal provider.

---

# 4. Domains supportati

I domain attualmente previsti sono:

- `sensor`
- `binary_sensor`
- `switch`
- `button`
- `select`
- `number`
- `text`
- `input_boolean`
- `input_button`
- `input_number`
- `input_select`
- `input_text`

## 4.1 sensor

Entità numerica o testuale usata per misura o stato continuo.

Esempio:

```yaml
sensor:
  - id: temp_raw
    name: Zone Temperature Raw
    provider: mqtt
    role: input
    source:
      topic: thermo/zone/01/temp_raw/state
```

## 4.2 binary_sensor

Entità booleana di stato.

Esempio:

```yaml
binary_sensor:
  - id: window_open
    name: Window Open
    provider: mqtt
    role: input
    source:
      topic: thermo/zone/01/window_open/state
```

Esempio derivato:

```yaml
binary_sensor:
  - id: cool_ready
    name: Cool Ready
    provider: derived
    role: state
    dependencies:
      - general_cool_enable
      - master_ac_cool_capable
```

## 4.3 switch

Entità booleana comandabile, tipicamente associata a un enable hardware o software.

```yaml
switch:
  - id: hardware_zone_ac_enable
    name: Hardware Zone AC Enable
    provider: config
    role: output
```

## 4.4 button

Entità impulsiva senza stato persistente significativo.

```yaml
button:
  - id: sync_request
    name: Sync Request
    provider: config
    role: output
```

## 4.5 select

Entità che espone una scelta tra valori discreti.

```yaml
select:
  - id: operating_profile
    name: Operating Profile
    provider: config
    role: state
    options:
      - eco
      - normal
      - boost
    initial: normal
```

## 4.6 number

Entità numerica configurabile.

```yaml
number:
  - id: setpoint_heat
    name: Heat Setpoint
    provider: config
    role: output
    min: 15
    max: 25
    step: 0.5
    initial: 20
```

## 4.7 text

Entità testuale configurabile.

```yaml
text:
  - id: zone_label
    name: Zone Label
    provider: config
    role: state
    initial: Living Room
```

## 4.8 input_boolean

Versione input-oriented di una entità booleana configurabile.

```yaml
input_boolean:
  - id: master_enable
    name: Master Enable
    provider: config
    role: input
    initial: true
```

## 4.9 input_button

Versione input-oriented di un pulsante.

```yaml
input_button:
  - id: reset_alarm
    name: Reset Alarm
    provider: config
    role: input
```

## 4.10 input_number

Versione input-oriented di una entità numerica.

```yaml
input_number:
  - id: temp_offset
    name: Temperature Offset
    provider: config
    role: input
    min: -5
    max: 5
    step: 0.1
    initial: 0
```

## 4.11 input_select

Versione input-oriented di una select.

```yaml
input_select:
  - id: common_mode
    name: Common Mode
    provider: config
    role: input
    options:
      - off
      - heat
      - cool
    initial: off
```

## 4.12 input_text

Versione input-oriented di un campo testuale.

```yaml
input_text:
  - id: debug_note
    name: Debug Note
    provider: config
    role: input
    initial: ""
```

---

# 5. Provider supportati

Il provider definisce **da dove nasce logicamente l'entità**.

I valori tipici previsti nel progetto sono:

- `mqtt`
- `config`
- `runtime`
- `derived`

## 5.1 mqtt

L'entità riceve il proprio valore da un topic o da una sorgente esterna collegata via MQTT.

```yaml
sensor:
  - id: humidity_raw
    name: Humidity Raw
    provider: mqtt
    role: input
    source:
      topic: thermo/zone/01/humidity_raw/state
```

## 5.2 config

L'entità appartiene alla configurazione dichiarativa del sistema.

```yaml
switch:
  - id: hardware_master_ac_enable
    name: Hardware Master AC Enable
    provider: config
    role: output
```

## 5.3 runtime

L'entità è calcolata o gestita dal runtime engine come stato operativo interno.

```yaml
binary_sensor:
  - id: general_cool_enable
    name: General Cool Enable
    provider: runtime
    role: state
    dependencies:
      - common_mode
```

## 5.4 derived

L'entità è esplicitamente derivata da altre entità attraverso dipendenze e futura evaluation logic.

```yaml
sensor:
  - id: temp_corrected
    name: Temperature Corrected
    provider: derived
    role: state
    dependencies:
      - temp_raw
      - temp_offset
```

---

# 6. Role supportati

Il role definisce **come l'entità viene usata nel modello logico**.

Valori previsti:

- `input`
- `output`
- `state`

## 6.1 input

Entità che rappresenta un ingresso logico al sistema.

Esempi:
- sensore fisico
- comando utente
- selettore di modalità

```yaml
sensor:
  - id: temp_raw
    name: Temperature Raw
    provider: mqtt
    role: input
```

## 6.2 output

Entità usata per comandare qualcosa.

Esempi:
- abilitazione hardware
- setpoint da inviare
- comando attuativo

```yaml
switch:
  - id: boiler_enable
    name: Boiler Enable
    provider: config
    role: output
```

## 6.3 state

Entità che rappresenta stato interno, spesso calcolato o aggregato.

```yaml
binary_sensor:
  - id: heat_ready
    name: Heat Ready
    provider: derived
    role: state
    dependencies:
      - boiler_enable
      - circulation_ok
```

---

# 7. Sintassi delle dependencies

Le dipendenze descrivono da quali altre entità dipende l'entità corrente.

## 7.1 Riferimento locale

Se la dipendenza è nella stessa istanza, si può usare il local id.

```yaml
dependencies:
  - temp_raw
  - temp_offset
```

Questo equivale logicamente a:

- `current_instance.temp_raw`
- `current_instance.temp_offset`

## 7.2 Riferimento assoluto namespaced

Per riferirsi a un'altra istanza si usa la forma:

```yaml
dependencies:
  - common.common_mode
  - zone_02.temp_raw
```

## 7.3 Esempio misto

```yaml
binary_sensor:
  - id: zone_cool_authorized
    name: Zone Cool Authorized
    provider: derived
    role: state
    dependencies:
      - temp_raw
      - common.common_mode
      - common.master_ac_cool_capable
```

In questo esempio:
- `temp_raw` è locale
- `common.common_mode` è assoluto
- `common.master_ac_cool_capable` è assoluto

## 7.4 Regole

Le dipendenze devono rispettare queste regole:

- ogni riferimento deve puntare a una entità esistente
- i riferimenti locali sono risolti rispetto all'istanza corrente
- i riferimenti assoluti devono usare `instance_id.local_id`
- le dipendenze duplicate dovrebbero essere evitate
- i cicli logici non dovrebbero essere introdotti nella configurazione

---

# 8. Source object

Il blocco `source` descrive la configurazione della sorgente dati quando l'entità non è puramente dichiarativa.

La forma esatta dipende dal tipo di provider e dall'evoluzione del progetto.

## 8.1 Caso MQTT base

```yaml
sensor:
  - id: temp_raw
    name: Temperature Raw
    provider: mqtt
    role: input
    source:
      topic: thermo/zone/01/temp_raw/state
```

## 8.2 Convenzione corrente

Nel progetto attuale il caso più importante è la presenza di `topic`.

Campi tipici attesi o futuri:

| Campo | Tipo | Significato |
|---|---|---|
| `topic` | string | Topic MQTT principale |
| `command_topic` | string | Topic di comando, se applicabile |
| `state_topic` | string | Topic di stato, se separato |
| `payload_map` | object | Eventuale mapping payload |

Nota: alcuni di questi campi possono essere pianificati ma non ancora implementati nel runtime.

---

# 9. Evaluation object

Il blocco `evaluation` è destinato alla futura definizione della logica di calcolo delle entità derivate o runtime.

Esempio concettuale:

```yaml
binary_sensor:
  - id: cool_ready
    name: Cool Ready
    provider: derived
    role: state
    dependencies:
      - general_cool_enable
      - master_ac_cool_capable
    evaluation:
      operator: and
```

Oppure:

```yaml
sensor:
  - id: temp_corrected
    name: Temperature Corrected
    provider: derived
    role: state
    dependencies:
      - temp_raw
      - temp_offset
    evaluation:
      operator: add
```

Nota importante:
- la sintassi definitiva di `evaluation` dipenderà dal runtime engine
- il configuration layer può limitarne la validazione o trattarla inizialmente come struttura libera controllata

---

# 10. Campi domain-specific

Alcuni domain supportano campi aggiuntivi.

## 10.1 `options`

Usato da:
- `select`
- `input_select`

```yaml
input_select:
  - id: common_mode
    name: Common Mode
    provider: config
    role: input
    options:
      - off
      - heat
      - cool
```

Regole raccomandate:
- ogni voce deve essere stringa
- evitare duplicati
- l'eventuale `initial` dovrebbe appartenere alla lista

## 10.2 `initial`

Usato da:
- `select`
- `number`
- `text`
- `input_boolean`
- `input_number`
- `input_select`
- `input_text`

Esempi:

```yaml
input_boolean:
  - id: master_enable
    name: Master Enable
    provider: config
    role: input
    initial: true
```

```yaml
input_select:
  - id: common_mode
    name: Common Mode
    provider: config
    role: input
    options: [off, heat, cool]
    initial: off
```

## 10.3 `min`, `max`, `step`

Usati da:
- `number`
- `input_number`

```yaml
input_number:
  - id: temp_offset
    name: Temperature Offset
    provider: config
    role: input
    min: -5
    max: 5
    step: 0.1
    initial: 0
```

Regole raccomandate:
- `min <= initial <= max` se tutti presenti
- `step > 0`
- `min <= max`

---

# 11. Expose flag

Alcune entità possono essere pensate come puramente interne, altre come esposte all'esterno.

Esempio:

```yaml
binary_sensor:
  - id: cool_ready
    name: Cool Ready
    provider: derived
    role: state
    expose: true
    dependencies:
      - general_cool_enable
      - master_ac_cool_capable
```

Uso raccomandato:
- `expose: true` per entità utili verso HA/UI
- `expose: false` per entità tecniche interne
- se omesso, il comportamento dipende dalla default policy del progetto

---

# 12. Esempi completi per dominio

## 12.1 sensor MQTT

```yaml
sensor:
  - id: temp_raw
    name: Zone Temperature Raw
    provider: mqtt
    role: input
    expose: true
    source:
      topic: thermo/zone/01/temp_raw/state
```

## 12.2 sensor derived

```yaml
sensor:
  - id: temp_corrected
    name: Zone Temperature Corrected
    provider: derived
    role: state
    expose: true
    dependencies:
      - temp_raw
      - temp_offset
    evaluation:
      operator: add
```

## 12.3 binary_sensor runtime

```yaml
binary_sensor:
  - id: general_cool_enable
    name: General Cool Enable
    provider: runtime
    role: state
    dependencies:
      - common_mode
```

## 12.4 switch config

```yaml
switch:
  - id: hardware_zone_ac_enable
    name: Hardware Zone AC Enable
    provider: config
    role: output
    expose: true
```

## 12.5 select config

```yaml
select:
  - id: operating_profile
    name: Operating Profile
    provider: config
    role: state
    options:
      - eco
      - normal
      - boost
    initial: normal
```

## 12.6 number config

```yaml
number:
  - id: heat_setpoint
    name: Heat Setpoint
    provider: config
    role: output
    min: 15
    max: 25
    step: 0.5
    initial: 20
```

## 12.7 text config

```yaml
text:
  - id: install_label
    name: Install Label
    provider: config
    role: state
    initial: Main Floor
```

## 12.8 input_boolean

```yaml
input_boolean:
  - id: manual_override
    name: Manual Override
    provider: config
    role: input
    initial: false
```

## 12.9 input_button

```yaml
input_button:
  - id: force_refresh
    name: Force Refresh
    provider: config
    role: input
```

## 12.10 input_number

```yaml
input_number:
  - id: temp_offset
    name: Temperature Offset
    provider: config
    role: input
    min: -5
    max: 5
    step: 0.1
    initial: 0
```

## 12.11 input_select

```yaml
input_select:
  - id: common_mode
    name: Common Mode
    provider: config
    role: input
    options:
      - off
      - heat
      - cool
    initial: off
```

## 12.12 input_text

```yaml
input_text:
  - id: operator_note
    name: Operator Note
    provider: config
    role: input
    initial: ""
```

---

# 13. Esempi completi per scenario

## 13.1 Caso zona base

```yaml
sensor:
  - id: temp_raw
    name: Zone Temperature Raw
    provider: mqtt
    role: input
    source:
      topic: thermo/zone/01/temp_raw/state

input_number:
  - id: temp_offset
    name: Temperature Offset
    provider: config
    role: input
    min: -5
    max: 5
    step: 0.1
    initial: 0

sensor:
  - id: temp_corrected
    name: Zone Temperature Corrected
    provider: derived
    role: state
    dependencies:
      - temp_raw
      - temp_offset
    evaluation:
      operator: add
```

## 13.2 Caso controllo raffrescamento

```yaml
input_select:
  - id: common_mode
    name: Common Mode
    provider: config
    role: input
    options: [off, heat, cool]
    initial: off

switch:
  - id: hardware_master_ac_enable
    name: Hardware Master AC Enable
    provider: config
    role: output

switch:
  - id: hardware_master_ac_cool_enable
    name: Hardware Master AC Cool Enable
    provider: config
    role: output

binary_sensor:
  - id: general_cool_enable
    name: General Cool Enable
    provider: runtime
    role: state
    dependencies:
      - common_mode

binary_sensor:
  - id: master_ac_cool_capable
    name: Master AC Cool Capable
    provider: runtime
    role: state
    dependencies:
      - hardware_master_ac_enable
      - hardware_master_ac_cool_enable

binary_sensor:
  - id: cool_ready
    name: Cool Ready
    provider: derived
    role: state
    dependencies:
      - general_cool_enable
      - master_ac_cool_capable
    evaluation:
      operator: and
```

---

# 14. Regole di qualità consigliate

Per mantenere i manifest puliti e robusti:

- usare `id` brevi ma semantici
- evitare abbreviazioni poco chiare
- usare `name` leggibili lato UI
- evitare entità con doppio significato
- mantenere coerenza tra `provider` e comportamento reale
- usare `dependencies` solo quando esiste una vera relazione logica
- preferire riferimenti locali quando l'entità è nella stessa istanza
- usare riferimenti assoluti solo quando necessario
- evitare cicli
- evitare duplicati nella stessa lista domain
- evitare collisioni tra naming locali che possano generare canonical id ambiguo

---

# 15. Errori comuni da evitare

## 15.1 Dipendenza inesistente

```yaml
dependencies:
  - temp_not_found
```

Errore: l'entità referenziata non esiste.

## 15.2 Riferimento assoluto malformato

```yaml
dependencies:
  - zone_01_temp_raw
```

Errore: se usi riferimento assoluto namespaced deve essere `zone_01.temp_raw`, non `zone_01_temp_raw`.

## 15.3 Initial non coerente con options

```yaml
input_select:
  - id: common_mode
    name: Common Mode
    provider: config
    role: input
    options: [off, heat, cool]
    initial: dry
```

Errore: `initial` non appartiene alla lista `options`.

## 15.4 Range numerico incoerente

```yaml
input_number:
  - id: temp_offset
    name: Temperature Offset
    provider: config
    role: input
    min: 5
    max: -5
```

Errore: `min` maggiore di `max`.

## 15.5 Duplicato locale nella stessa istanza

```yaml
sensor:
  - id: temp_raw
    name: Temperature Raw
    provider: mqtt
    role: input

sensor:
  - id: temp_raw
    name: Temperature Raw Duplicate
    provider: mqtt
    role: input
```

Errore: collisione di id locale.

---

# 16. Convenzioni raccomandate

## 16.1 Naming

Pattern raccomandati:
- `temp_raw`
- `temp_corrected`
- `humidity_raw`
- `manual_override`
- `hardware_master_ac_enable`

## 16.2 Suffissi utili

Convenzioni consigliate:
- `_raw` per misure grezze
- `_corrected` per valori compensati
- `_enable` per abilitazioni
- `_ready` per stati di readiness
- `_capable` per capacità o compatibilità
- `_offset` per correzioni additive

## 16.3 Organizzazione logica

Conviene separare:
- entità di input fisico
- entità di configurazione
- entità runtime
- entità derived

Questo rende il manifest più leggibile e aiuta il debug.

---

# 17. Template completo di riferimento

```yaml
sensor:
  - id: temp_raw
    name: Zone Temperature Raw
    provider: mqtt
    role: input
    expose: true
    source:
      topic: thermo/zone/01/temp_raw/state

  - id: temp_corrected
    name: Zone Temperature Corrected
    provider: derived
    role: state
    expose: true
    dependencies:
      - temp_raw
      - temp_offset
    evaluation:
      operator: add

binary_sensor:
  - id: cool_ready
    name: Cool Ready
    provider: derived
    role: state
    expose: true
    dependencies:
      - common.common_mode
      - hardware_zone_ac_enable
    evaluation:
      operator: and

switch:
  - id: hardware_zone_ac_enable
    name: Hardware Zone AC Enable
    provider: config
    role: output
    expose: true

input_number:
  - id: temp_offset
    name: Temperature Offset
    provider: config
    role: input
    min: -5
    max: 5
    step: 0.1
    initial: 0

input_select:
  - id: zone_mode
    name: Zone Mode
    provider: config
    role: input
    options:
      - off
      - auto
      - cool
      - heat
    initial: auto

input_boolean:
  - id: manual_override
    name: Manual Override
    provider: config
    role: input
    initial: false

input_button:
  - id: force_recompute
    name: Force Recompute
    provider: config
    role: input

input_text:
  - id: debug_note
    name: Debug Note
    provider: config
    role: input
    initial: ""
```

---

# 18. Stato attuale e note evolutive

Questo documento descrive la sintassi target del modulo e include sia:

- casi già presenti nel progetto
- casi supportati dal modello attuale
- casi previsti come naturale estensione del runtime

In particolare:

- `dependencies` è già un concetto strutturale centrale
- `source.topic` è già un caso concreto importante
- `evaluation` è concettualmente definita ma dipende dalla futura implementazione del runtime
- alcuni campi specifici possono essere raffinati quando verrà introdotto l'Entity Registry

Per questo motivo conviene distinguere tra:

- **sintassi dichiarativa stabile**
- **semantica runtime in evoluzione**

Il configuration layer deve restare il più possibile stabile e leggibile, anche mentre il runtime cresce.