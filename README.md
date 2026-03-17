# ActiveThermo v2

ActiveThermo è un motore software per il controllo intelligente di sistemi HVAC domestici e multi‑zona.

Il progetto nasce per realizzare un sistema di gestione termica avanzato che integri:

- riscaldamento
- raffrescamento
- ventilazione
- automazione domestica
- sensori distribuiti

Il sistema è progettato per funzionare in integrazione con:

- MQTT
- Home Assistant
- dispositivi hardware custom
- sistemi HVAC commerciali

---

# Architettura del progetto

Il sistema è composto da due livelli principali.

## Configuration Layer

Responsabile della lettura e validazione della configurazione del sistema.

Modulo principale:

entity_config_assembler

Questo modulo:

- carica i file YAML
- valida lo schema
- normalizza le entità
- risolve le dipendenze
- costruisce la configurazione finale

Output:

AssembledConfiguration

---

## Runtime Layer (in sviluppo)

Responsabile della logica operativa del sistema.

Componenti previsti:

- Entity Registry
- State Engine
- Dependency Propagation
- MQTT Integration
- Home Assistant Bridge

---

# Struttura del progetto

Active_thermo/

config/
system/
entity_config_assembler/
docs/
tests/

---

# Stato del progetto

| Modulo | Stato |
|------|------|
entity_config_assembler | completato
entity_registry | in sviluppo
runtime_engine | pianificato

---

# Obiettivi del progetto

ActiveThermo punta a diventare una piattaforma modulare per:

- controllo HVAC multi‑zona
- building automation
- ottimizzazione energetica
- integrazione domotica avanzata