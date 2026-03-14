# PROJECT LOG — Avaluador de Repositoris

Aquest document registra les decisions tècniques i l'evolució del projecte.

Objectiu del projecte:
Construir una eina Python per analitzar repositoris d'alumnes i detectar evidències d'activitats.

---

# Estat actual del projecte

Arquitectura actual:

main.py
↓
ReposLocator
↓
DetectorEvidencies
↓
resultats a consola

Estructura del repo:

core/
    repos_locator.py
    detector_evidencies.py

data/
    repos_map.example.json
    repos_map.json (local)

repos/
    repositoris de prova

---

# Components implementats

## ReposLocator

Responsabilitat:
Localitzar el repositori associat a cada unitat d'avaluació.

Entrada:
data/repos_map.json

Sortida:
Path al repositori.

---

## DetectorEvidencies

Responsabilitat:
Escanejar un repositori i detectar fitxers candidats a evidència.

Primera versió:
detecció d'imatges (.png, .jpg).

---

# Motor actual

El motor actual executa:

python main.py

Flux:

repos_map.json
→ ReposLocator
→ DetectorEvidencies
→ output a consola

---

# Properes funcionalitats previstes

1️⃣ Definir regles d'evidències

config/regles_evidencies.json

2️⃣ Sistema de validació

esperat vs trobat

3️⃣ Generació d'informes

CSV
JSON
Markdown

4️⃣ Suport per múltiples mòduls

SMX
DAM

---

# Decisions de disseny

Separació entre:

repos_map.example.json → versionat
repos_map.json → configuració local (gitignore)

Motiu:
evitar paths locals dins del repo.