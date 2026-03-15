# Eina docent per a l’avaluació assistida de repositoris Git d’alumnes.

Aquest projecte té com a objectiu **reduir radicalment el temps de correcció d’activitats entregades en repositoris Git**, mantenint al mateix temps el criteri docent.

El sistema combina:

- detecció automàtica d’evidències
- revisió assistida pel professor
- registre estructurat de notes

El projecte està pensat per utilitzar-se en entorns docents com:

- **SMX** (Sistemes Microinformàtics i Xarxes)
- **DAM** (Desenvolupament d’Aplicacions Multiplataforma)

El motor de correcció és **independent del cicle** i funciona mitjançant fitxers de configuració.

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

# Avantatge del model

El motor només treballa amb:

```
RA + unitat_avaluacio
```

Per tant funciona igual per:

- repositoris individuals
- repositoris de grup

---

# Model de navegació

La correcció no es fa per alumne.

Es fa per **Resultat d’Aprenentatge (RA)**.

Ordre de revisió:

```
RA → unitats d’avaluació → evidència
```

Avantatges:

- criteri homogeni
- comparació entre alumnes
- correcció més ràpida

---

# Evidències

Cada RA defineix una **evidència esperada**.

Exemple:

```
05_comunicacio/correu_enviat.png
```

El sistema comprova si existeix exactament.

Si no existeix, es busquen **evidències alternatives**.

---

# Cerca d’evidències alternatives

El sistema buscarà al repositori:

```
*.png
*.jpg
*.jpeg
```

Aquestes imatges es mostraran com a possibles evidències.

El professor decidirà si alguna és vàlida.

---

# Tipus de casos possibles

El sistema contempla quatre situacions:

### Cas 1 — evidència perfecta

```
estructura correcta
evidència correcta
```

### Cas 2 — evidència correcta però mal ubicada

```
estructura incorrecta
evidència correcta
```

### Cas 3 — evidència incorrecta

```
imatge present però no vàlida
```

### Cas 4 — cap evidència

```
no hi ha cap fitxer utilitzable
```

---

# Visualització d’evidències

Quan el professor selecciona una evidència:

la imatge s’obre amb el visor del sistema operatiu.

No es requereix cap interfície gràfica complexa.

---

# Persistència de correccions

Les correccions es guarden en un fitxer estructurat.

Per exemple:

```
correccions.json
```

Això permet:

- reprendre correccions
- no repetir evidències ja revisades
- modificar notes ja assignades

---

# Arquitectura del projecte

El projecte es divideix en:

```
motor de correcció
+
configuració docent
```

---

# Implementació actual del projecte

Tot i que el README descriu el **model conceptual complet del motor d’avaluació**, el projecte ja disposa d’una **implementació funcional parcial** utilitzada per corregir activitats reals.

Actualment el sistema permet **avaluar repositoris clonats de GitHub Classroom i generar notes automàticament**.

Flux actual utilitzat a SMX:

```
gh classroom clone student-repos
↓
repos/
↓
tools/evaluate_repos.py
↓
data/notes_smx.csv
data/notes_smx.md
```

Aquest script analitza els repositoris clonats i detecta evidències definides a:

```
data/rules.json
```

Els alumnes es mapegen mitjançant:

```
data/repos_map.json
```

A partir d'aquesta informació el sistema:

1. escaneja cada repositori
2. comprova evidències definides per cada RA
3. calcula la puntuació
4. genera un informe de notes

---

# Visualització dels resultats

Per facilitar la lectura dels resultats, el sistema utilitza símbols:

```
✔ evidència trobada
✘ evidència absent
```

A més, el sistema mostra **Nom Cognoms de l’alumne** en lloc del nom del repositori.

---

# Estructura actual del repositori

```
avaluador_repos/

core/
    repos_locator.py
    detector_evidencies.py
    buscador_alternatives.py
    navegador_ra.py
    visor_imatges.py
    registre_avaluacions.py

tools/
    evaluate_repos.py

data/
    repos_map.json
    rules.json
    corrections.json

repos/
    repositoris clonats de GitHub Classroom

main.py
```

---

# Configuració per cicle

Els mòduls i RA es defineixen en fitxers de configuració.

Exemple:

```
config/smx.json
config/dam.json
```

Aquests fitxers defineixen:

- unitats d’avaluació
- mòduls
- resultats d’aprenentatge
- evidències esperades

---

# Mapatge unitat → repositori

El fitxer:

```
data/repos_map.json
```

defineix quin repositori correspon a cada unitat d’avaluació.

Exemple:

```
{
  "github-user-alumne-1": "smx-sprint-t2-github-user-alumne-1",
  "github-user-alumne-2": "smx-sprint-t2-github-user-alumne-2"
}
```

---

# Flux conceptual complet del sistema

El motor complet seguirà aquest flux:

```
0 carregar correccions existents
1 carregar configuració del cicle
2 construir unitats d’avaluació
3 construir la llista de RA
4 generar totes les combinacions (RA, unitat)
5 localitzar repositori associat
6 detectar evidència exacta
7 cercar evidències alternatives
8 mostrar evidència al professor
9 registrar nota i comentari
10 guardar correcció i continuar
```

---

# Estat actual del projecte

El projecte es troba en una fase **intermèdia**:

- el **model conceptual del motor d’avaluació està definit**
- existeix **una implementació funcional per generar notes automàtiques**
- el sistema ja s’utilitza per corregir activitats de SMX

El desenvolupament futur integrarà aquesta implementació amb el motor complet d’avaluació assistida.

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