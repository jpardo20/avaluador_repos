# Eina docent per a l’avaluació assistida de repositoris Git d’alumnes

Aquest projecte té com a objectiu **reduir radicalment el temps de correcció d’activitats entregades en repositoris Git**, mantenint al mateix temps el criteri docent.

El sistema combina:

- detecció automàtica d’evidències
- revisió assistida pel professor
- registre estructurat de notes

El projecte està pensat per utilitzar-se en entorns docents com:

- **SMX** (Sistemes Microinformàtics i Xarxes)
- **DAM** (Desenvolupament d’Aplicacions Multiplataforma)

El motor de correcció és **independent del cicle** i funciona mitjançant configuració.

---

# Objectiu del projecte

Quan els alumnes treballen amb repositoris Git, sovint entreguen evidències com:

- captures de pantalla
- documents
- scripts
- informes
- configuracions

Aquestes evidències es relacionen amb **Resultats d’Aprenentatge (RA)** dels mòduls.

Els scripts automàtics clàssics només poden comprovar:

```
existeix el fitxer / no existeix
```

Però això té problemes:

- els alumnes canvien noms de fitxer
- guarden evidències en carpetes incorrectes
- l’evidència pot existir però amb un nom diferent

Això provoca dues situacions dolentes:

1. correccions automàtiques injustes
2. correcció manual molt lenta

---

# Solució proposada

Aquest projecte implementa un sistema **híbrid**:

```
detecció automàtica
+
criteri docent
```

Flux de correcció:

```
script detecta evidències
↓
mostra evidència al professor
↓
el professor valida la correcta
↓
assigna nota
↓
registre estructurat
```

Això permet:

- automatitzar gran part de la feina
- mantenir criteri pedagògic
- reduir molt el temps de correcció

---

# Concepte clau: unitat d’avaluació

El sistema **no treballa amb repositoris**, sinó amb **unitats d’avaluació**.

Una unitat d’avaluació pot ser:

- un alumne
- un grup

El repositori és només **la font d’evidències**.

---

# SMX

En SMX els repositoris són individuals.

```
unitat_avaluacio = alumne
repo = repositori de l’alumne
```

---

# DAM

En DAM els repositoris poden ser de grup.

```
unitat_avaluacio = grup
repo = repositori del grup
```

---

# Model de navegació

La correcció es fa per **Resultat d’Aprenentatge (RA)**.

Ordre de revisió:

```
RA → unitats d’avaluació → evidència
```

Avantatges:

- criteri homogeni
- comparació entre alumnes
- correcció més ràpida

---

# Arquitectura del motor

El motor s’organitza en components independents.

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

# Components del sistema

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

Exemple de sortida:

```
[
    "05_comunicacio/correu_enviat.png",
    "01_document/informe.docx"
]
```

---

## RuleEngine

Responsabilitat:

Aplicar regles d’evidència definides a configuració.

Exemple de resultat:

```
{
    "status": "exact_match",
    "file": "05_comunicacio/correu_enviat.png",
    "alternatives": []
}
```

Possibles resultats:

```
exact_match
alternative_found
no_evidence
```

---

## RulesRegistry

Responsabilitat:

Carregar les regles d’evidència definides per cada RA.

Fitxer:

```
data/rules.json
```

Exemple:

```
{
  "unitat-1": {
    "expected_path": "05_comunicacio/correu_enviat.png",
    "evidence_type": "image"
  }
}
```

Aquest sistema permet:

- modificar evidències esperades
- adaptar-se a diferents mòduls
- evitar canvis de codi

---

## CorrectionRegistry

Responsabilitat:

Guardar i recuperar les correccions realitzades.

Fitxer:

```
data/corrections.json
```

Permet:

- reprendre correccions
- evitar repetir revisions
- modificar notes

---

# Estructura del repositori

```
avaluador_repos/

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

# Flux complet del sistema

```
0 carregar correccions existents

1 carregar configuració de regles

2 carregar mapatge unitat → repositori

3 generar llista de unitats

4 escanejar repositori

5 aplicar regles d’evidència

6 mostrar resultats al professor

7 registrar nota i comentari

8 guardar correcció
```

---

# Objectiu final

Construir una eina docent que combini:

```
repositoris Git d’alumnes
+
detecció automàtica d’evidències
+
avaluació docent assistida
+
registre estructurat de notes
```

per millorar:

- eficiència de correcció
- justícia de l’avaluació
- coherència pedagògica