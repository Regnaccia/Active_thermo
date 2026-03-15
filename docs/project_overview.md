# Project Overview

ActiveThermo è un sistema software progettato per gestire sistemi HVAC domestici e multi‑zona.

Il progetto nasce con l'obiettivo di costruire un motore di controllo termico avanzato che integri:

- sensori distribuiti
- attuatori HVAC
- logica di controllo
- integrazione domotica
- algoritmi di ottimizzazione energetica

---

# Filosofia del progetto

Il progetto separa chiaramente due livelli.

## Configuration Layer

Responsabile della descrizione del sistema.

Qui si definiscono:

- entità
- sensori
- attuatori
- dipendenze logiche

Questo livello è completamente statico.

---

## Runtime Layer

Responsabile dell'esecuzione del sistema.

Funzioni:

- gestione dello stato
- propagazione delle dipendenze
- valutazione delle entità derivate
- integrazione MQTT
- comunicazione con Home Assistant

---

# Concetto di Entity

Il sistema è modellato tramite entità.

Una entità rappresenta un elemento logico del sistema:

Esempi:

- sensore temperatura
- switch hardware
- modalità operativa
- stato derivato
- comando utente

Ogni entità ha:

- un dominio
- un provider
- un ruolo
- eventuali dipendenze

---

# Principio fondamentale

Il sistema è costruito come un grafo di dipendenze tra entità.