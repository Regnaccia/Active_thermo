# Entity Config Assembler

Il modulo entity_config_assembler è responsabile della costruzione della configurazione del sistema.

Questo modulo è il configuration compiler di ActiveThermo.

---

# Responsabilità

Il modulo esegue le seguenti operazioni:

1. Caricamento configurazione
2. Validazione schema
3. Normalizzazione entità
4. Risoluzione dipendenze
5. Verifica integrità
6. Costruzione configurazione finale

---

# Input

File YAML presenti nella directory config.

---

# Output

Il modulo produce un oggetto:

AssembledConfiguration

che contiene:

- configurazione sistema
- configurazione mqtt
- lista istanze
- lista entità
- dipendenze risolte

---

# Flusso di esecuzione

load system config  
load mqtt config  
load instance package  
load instance router  
load entity manifests  
validate entities  
resolve dependencies  
build configuration