# avaluador_repos

Eina docent per a l’avaluació assistida de repositoris Git d’alumnes.

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

## Objectiu del projecte

Quan els alumnes treballen amb repositoris Git, sovint entreguen evidències com:

- captures de pantalla
- documents
- scripts
- informes
- configuracions

Aquestes evidències es relacionen amb **Resultats d’Aprenentatge (RA)** dels mòduls.

Els scripts automàtics clàssics només poden comprovar:

```bash
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

## Solució proposada

Aquest projecte implementa un sistema **híbrid**:

```bash
detector automàtic
+
criteri docent
```

Flux de correcció:

```bash
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

## Concepte clau: unitat d’avaluació

El sistema **no treballa amb repositoris**, sinó amb **unitats d’avaluació**.

Una unitat d’avaluació pot ser:

- un alumne
- un grup

El repositori és només **la font d’evidències**.

---

## SMX

En SMX els repositoris són individuals.

```bash
unitat_avaluacio = alumne
repo = repositori de l’alumne
```

---

## DAM

En DAM els repositoris poden ser de grup.

```bash
unitat_avaluacio = grup
repo = repositori del grup
```

---

## Avantatge del model

El motor només treballa amb:

```bash
RA + unitat_avaluacio
```

Per tant funciona igual per:

- repositoris individuals
- repositoris de grup

---

## Model de navegació

La correcció no es fa per alumne.

Es fa per **Resultat d’Aprenentatge (RA)**.

Ordre de revisió:

```bash
RA → unitats d’avaluació → evidència
```

Exemple:

```bash
RA5 Comunicació

github-user-alumne-1
github-user-alumne-2
github-user-alumne-3
github-user-alumne-4
```

Avantatges:

- criteri homogeni
- comparació entre alumnes
- correcció més ràpida

---

## Evidències

Cada RA defineix una **evidència esperada**.

Exemple:

```bash
05_comunicacio/correu_enviat.png
```

El sistema comprova si existeix exactament.

Si no existeix, es busquen **evidències alternatives**.

---

## Cerca d’evidències alternatives

El sistema buscarà al repositori:

```bash
*.png
*.jpg
*.jpeg
```

Aquestes imatges es mostraran com a possibles evidències.

El professor decidirà si alguna és vàlida.

---

## Tipus de casos possibles

El sistema contempla quatre situacions:

### Cas 1 — evidència perfecta

```bash
estructura correcta
evidència correcta
```

---

### Cas 2 — evidència correcta però mal ubicada

```bash
estructura incorrecta
evidència correcta
```

---

### Cas 3 — evidència incorrecta

```bash
imatge present però no vàlida
```

---

### Cas 4 — cap evidència

```bash
no hi ha cap fitxer utilitzable
```

---

## Visualització d’evidències

Quan el professor selecciona una evidència:

la imatge s’obre amb el visor del sistema operatiu.

No es requereix cap interfície gràfica complexa.

---

## Persistència de correccions

Les correccions es guarden en un fitxer estructurat.

Per exemple:

```bash
correccions.json
```

Això permet:

- reprendre correccions
- no repetir evidències ja revisades
- modificar notes ja assignades

---

## Arquitectura del projecte

El projecte es divideix en:

```bash
motor de correcció
+
configuració docent
```

---

## Estructura del repositori

```bash
avaluador_repos/

core/
    repos_locator.py
    detector_evidencies.py
    buscador_alternatives.py
    navegador_ra.py
    visor_imatges.py
    registre_avaluacions.py

config/
    smx.json
    dam.json

data/
    repos_map.json
    correccions.json

main.py
```

---

## Configuració per cicle

Els mòduls i RA es defineixen en fitxers de configuració.

Exemple:

```bash
config/smx.json
config/dam.json
```

Aquests fitxers defineixen:

- unitats d’avaluació
- mòduls
- resultats d’aprenentatge
- evidències esperades

---

## Mapatge unitat → repositori

El fitxer:

```bash
data/repos_map.json
```

defineix quin repositori correspon a cada unitat d’avaluació.

Exemple:

```bash
{
  "github-user-alumne-1": "smx-sprint-t2-github-user-alumne-1",
  "github-user-alumne-2": "smx-sprint-t2-github-user-alumne-2"
}
```

Per DAM podria ser:

```bash
{
  "grup-1": "github-user-alumne-grup-1",
  "grup-2": "github-user-alumne-grup-2"
}
```

---

## Flux complet del sistema

Per evitar redissenyar l’eina mentre es programa, el sistema seguirà aquest flux.

```bash
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

## Estat actual del projecte

Aquest repositori conté **la primera versió conceptual del sistema**.

En aquesta fase es definirà:

- arquitectura
- model de dades
- flux de correcció

Abans d’implementar el motor complet.

---

## Objectiu final

Construir una eina docent que combini:

```bash
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
- coherència pedagògica.
