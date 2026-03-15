# Decision Log

Questo documento registra le principali decisioni architetturali del progetto.

---

# Decisione 1

Separazione tra configuration layer e runtime layer.

Motivazione:

- maggiore modularità
- maggiore testabilità
- configurazione completamente dichiarativa

---

# Decisione 2

Utilizzo di YAML per la configurazione.

Motivazione:

- leggibilità
- semplicità
- diffusione nello sviluppo infrastrutturale

---

# Decisione 3

Sistema basato su dependency graph.

Motivazione:

permettere:

- entità derivate
- propagazione stato
- valutazioni automatiche