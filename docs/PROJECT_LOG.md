# PROJECT LOG — Avaluador de Repositoris

Aquest document registra les decisions tècniques i l’evolució del projecte.

Objectiu:

Construir una eina Python per analitzar repositoris d’alumnes i detectar evidències d’activitats associades a Resultats d’Aprenentatge (RA).

---

# Estat actual del projecte

Arquitectura actual:

```
main.py
↓
ReposLocator
↓
RepoScanner
↓
RuleEngine
↓
CorrectionRegistry
```

---

# Estructura actual del repositori

```
core/
    repos_locator.py
    repo_scanner.py
    rule_engine.py
    rules_registry.py
    correction_registry.py

data/
    repos_map.json
    rules.json
    corrections.json

repos/
    repositoris de prova

main.py
```

---

# Components implementats

## ReposLocator

Responsabilitat:

Localitzar el repositori associat a cada unitat d’avaluació.

Entrada:

```
data/repos_map.json
```

Sortida:

```
path al repositori
```

---

## RepoScanner

Responsabilitat:

Escanejar el repositori i generar un inventari de fitxers.

Permet:

- detectar evidències
- buscar alternatives
- desacoblar el motor de la estructura del repo

---

## RulesRegistry

Responsabilitat:

Carregar les regles d’evidència definides a configuració.

Fitxer:

```
data/rules.json
```

Aquest component desacobla:

```
regles d’avaluació
```

del

```
codi Python
```

---

## RuleEngine

Responsabilitat:

Aplicar les regles sobre l’inventari de fitxers.

Resultats possibles:

```
exact_match
alternative_found
no_evidence
```

Sortida:

estructura amb evidència detectada.

---

## CorrectionRegistry

Responsabilitat:

Persistir les correccions realitzades pel professor.

Fitxer:

```
data/corrections.json
```

Permet:

- reprendre correccions
- evitar repetir revisions
- mantenir historial

---

# Decisions de disseny

Separació entre:

```
lògica del motor
```

i

```
configuració docent
```

Això permet:

- adaptar el sistema a diferents cicles
- modificar evidències sense tocar el codi
- reutilitzar el motor

---

# Decisions importants

## Principi de disseny del motor

El motor d’avaluació segueix tres principis de disseny.

### 1. Desacoblament

La lògica del motor Python no conté informació docent.

Tot el criteri d’avaluació es defineix en fitxers de configuració:

- rules.json
- repos_map.json
- config_smx.json
- config_dam.json

Això permet reutilitzar el motor en diferents cicles i mòduls sense modificar el codi.

---

### 2. Robustesa davant repositoris imperfectes

Els repositoris d’alumnes sovint tenen problemes com:

- noms de fitxer incorrectes
- evidències en carpetes incorrectes
- estructures no exactament iguals a l’enunciat

Per aquest motiu el motor implementa dos nivells de detecció:

1. coincidència exacta
2. cerca d’evidències alternatives

Això evita falsos negatius en la correcció automàtica.

---

### 3. Correcció assistida

El sistema no intenta substituir el professor.

El sistema:

- detecta evidències
- presenta possibles alternatives
- registra la decisió docent

Això permet reduir el temps de correcció mantenint el criteri pedagògic.

## Unitat d’avaluació abstracta

El motor treballa amb:

```
RA + unitat d’avaluació
```

Una unitat pot ser:

```
alumne
grup
```

Això permet suportar:

- repositoris individuals
- repositoris de grup

sense modificar el motor.

---

# Properes funcionalitats previstes

1️⃣ sistema de revisió assistida

2️⃣ visor automàtic d’evidències

3️⃣ generació d’informes

```
CSV
JSON
Markdown
```

4️⃣ suport per múltiples mòduls

```
SMX
DAM
```

---

# Estat del projecte

El projecte es troba en fase de **motor funcional inicial**.

Ja existeixen:

- localització de repositoris
- escaneig de fitxers
- aplicació de regles
- registre de correccions

Els següents passos se centraran en:

- millorar la revisió assistida
- generar informes automàtics
- integrar múltiples mòduls i RA.

---

# Integració del motor de notes SMX

S’ha implementat un script per avaluar automàticament repositoris clonats de GitHub Classroom.

Components principals:

- `tools/evaluate_repos.py`
- `data/rules.json`
- `data/repos_map.json`

El sistema:

1. Escaneja repositoris clonats.
2. Aplica regles definides en JSON.
3. Calcula notes per RA.
4. Exporta resultats a CSV i Markdown.

Aquest motor ja s’està utilitzant per corregir activitats del mòdul SMX.


---

# Integració de l’exportador de notes per RA

S’ha implementat un component nou:

tools/notes_exporter.py

Aquest script transforma la informació guardada a:

data/corrections.json

en informes de notes utilitzables.

El sistema:

1. llegeix les correccions registrades
2. reorganitza la informació per unitat d’avaluació
3. calcula el total de punts
4. genera informes

Fitxers generats:

data/notes_smx.csv
data/notes_smx.md

Aquests informes mostren les notes per Resultat d’Aprenentatge (RA).
