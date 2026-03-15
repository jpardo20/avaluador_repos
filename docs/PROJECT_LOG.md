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
