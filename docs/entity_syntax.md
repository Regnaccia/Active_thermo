# Entity Syntax

Questo documento descrive la sintassi delle entità nei file YAML.

---

# Struttura base

sensor:
  - id: temp_raw
    name: Temperature Raw
    provider: mqtt
    role: input

---

# Campi obbligatori

| Campo | Descrizione |
|------|-------------|
id | identificatore locale
name | nome leggibile
provider | origine del dato
role | ruolo logico

---

# Domini supportati

sensor  
binary_sensor  
switch  
select  
number  
text  
input_boolean  
input_number  
input_select  
input_text  
input_button