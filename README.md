# MathArt

**Génération d'art animé à partir d'équations, et extraction des équations cachées dans les images.**

![Python](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows-0078D6?logo=windows&logoColor=white)

MathArt est une application desktop Windows qui relie mathématiques, art génératif et vision par ordinateur : elle produit des visuels animés à partir de fractales, de courbes paramétriques et de systèmes dynamiques, et retrouve une description mathématique des formes d'une image importée.

![Demo](docs/screenshots/demo.gif)

## Le principe

Un même objet mathématique peut être lu dans deux sens. Dans le sens direct, une équation (un ensemble de Julia, une courbe de Lissajous, l'attracteur de Lorenz) est évaluée et rendue à l'écran sous forme d'image animée. Dans le sens inverse, une forme observée (le contour d'une feuille, la crête d'une vague, la spirale d'un coquillage) est approchée par une représentation mathématique compacte.

Le **mode Créatif** exploite le sens direct. Chaque œuvre est décrite par un *preset* : un document JSON validé qui contient le type de générateur, ses paramètres, sa palette et son animation. Plusieurs couches peuvent être fusionnées (additif, multiply, screen) et soumises à des symétries (radiale k-fold, miroir). Un drone ambient synthétisé par numpy accompagne le visuel pour le focus et la méditation.

Le **mode Analyse** exploite le sens inverse. Une image est segmentée (OpenCV, PyTorch), son contour est extrait, puis décomposé en série de Fourier. Les coefficients dominants fournissent une approximation du contour dont l'erreur est mesurée. Cette représentation peut être rejouée dans le mode Créatif : une feuille devient un preset, et inversement.

Tout fonctionne en local : aucun compte, aucun service en ligne, aucune télémétrie.

## Fonctionnalités

### 🎨 Mode Créatif

- Générateurs : fractales (Mandelbrot, Julia, rendu GLSL), courbes paramétriques (Lissajous, épicycloïdes), systèmes dynamiques (Lorenz, Rössler), reconstruction depuis des coefficients de Fourier, image importée avec traitements.
- Composition par fusion de couches : modes additif, multiply et screen.
- Symétries : radiale (k-fold) et miroir.
- Bibliothèque de presets visuels et audio : création, édition, duplication, import et export.
- Drones ambient générés par synthèse (numpy), avec import de fichiers WAV et normalisation du volume.

### 🔬 Mode Analyse

- Import d'une image (feuille, vague, coquillage, nuage, etc.).
- Segmentation par OpenCV, avec options YOLO et DINOv2 (PyTorch, CPU par défaut).
- Extraction de contour et décomposition en série de Fourier.
- Reconstruction animée du contour à partir d'un nombre réglable d'harmoniques.
- Mesure de l'erreur d'approximation (RMSE) et identification des harmoniques dominantes.

### 🎯 Mode Focus

- Minuteur Pomodoro intégré (anneau de progression).
- Mode plein écran sans distraction.
- Raccourcis clavier pour toutes les actions courantes.

### 📄 Rapports

- Génération de rapports autoportants en HTML et PDF.
- Formules, spectres, formes d'onde et métriques d'erreur inclus (voir [Rapports scientifiques](#rapports-scientifiques)).

### Données

- Persistance *local-first* dans `%APPDATA%\MathArt`.
- Écritures JSON atomiques, cache des images et des décompositions de Fourier.

## Installation

### Prérequis

- Windows 10 ou 11 (64 bits)
- Python 3.11 ou supérieur
- Git

### Depuis les sources

```powershell
git clone https://github.com/soirfaneabdallah/mathart.git
cd MathArt

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
```

Le fichier `requirements.txt` est unique et installe PyTorch en version **CPU** par défaut :

```text
--extra-index-url https://download.pytorch.org/whl/cpu

PySide6>=6.6
numpy>=1.26
scipy>=1.11
opencv-python>=4.9
torch>=2.2
torchvision>=0.17
pydantic>=2.5
Jinja2>=3.1
WeasyPrint>=61
matplotlib>=3.8
```

> WeasyPrint dépend de bibliothèques GTK sous Windows. Si l'export PDF échoue, consulter la [documentation de WeasyPrint](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows). L'export HTML n'est pas concerné.

### Support GPU (optionnel)

Le CPU suffit pour l'ensemble des fonctionnalités. Pour accélérer la segmentation avec YOLO ou DINOv2, remplacer PyTorch par une version CUDA. Choisir l'index correspondant à votre pilote sur [pytorch.org](https://pytorch.org/get-started/locally/) :

```powershell
pip uninstall -y torch torchvision
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

### Modèles de vision (optionnel)

La segmentation OpenCV fonctionne sans téléchargement. Pour YOLO et DINOv2 :

```powershell
python scripts/download_models.py
```

### Installeur Windows

Un installeur est produit avec PyInstaller puis Inno Setup :

```powershell
pip install pyinstaller
python scripts/build.py
```

La sortie est écrite dans `build/windows/MathArt/`.

## Utilisation

### Démarrage rapide

```powershell
python main.py
```

1. Depuis l'accueil, choisir **Nouveau** ou **Reprendre** la dernière session.
2. En mode Créatif, sélectionner un preset dans la bibliothèque et ajuster ses paramètres.
3. Ajouter une couche, choisir un mode de fusion et activer une symétrie si besoin.
4. Lancer un drone audio, puis démarrer le minuteur Pomodoro.
5. En mode Analyse, importer une image, lancer l'extraction, puis générer un rapport.

### Exemple de preset

Un preset est un fichier JSON validé par un schéma Pydantic :

```json
{
  "name": "Lissajous 3:2",
  "type": "parametrique",
  "params": { "a": 3, "b": 2, "delta": 1.5708, "amplitude": 0.8 },
  "palette": ["#12121c", "#7c5cff", "#2ee6a6"],
  "animation": { "speed": 0.5, "loop": true },
  "symmetry": { "kind": "radial", "k": 6 }
}
```

Le cœur de l'application est indépendant de Qt et peut être utilisé en script :

```python
from core.presets.schema import VisualPreset
from core.visual.pipeline import rendre

preset = VisualPreset.model_validate_json(open("lissajous.json", encoding="utf-8").read())
buffer = rendre(preset, t=0.0)   # image RGBA, ndarray (H, W, 4)
```

### Raccourcis clavier

Les raccourcis par défaut sont modifiables dans les préférences.

| Action | Raccourci |
|---|---|
| Mode Créatif / Analyse | `Ctrl+1` / `Ctrl+2` |
| Bibliothèque de presets | `Ctrl+L` |
| Nouveau preset | `Ctrl+N` |
| Importer une image | `Ctrl+O` |
| Lecture / pause de l'animation | `Espace` |
| Lecture / pause audio | `Ctrl+Espace` |
| Volume + / − | `Ctrl+↑` / `Ctrl+↓` |
| Démarrer / arrêter le Pomodoro | `Ctrl+P` |
| Plein écran | `F11` |
| Quitter le plein écran | `Échap` |
| Exporter une image | `Ctrl+E` |
| Générer un rapport | `Ctrl+R` |
| Préférences | `Ctrl+,` |

## Architecture

```text
MathArt/
├── main.py            # point d'entrée
├── app/               # bootstrap Qt, fenêtre, état, thème, raccourcis
├── ui/                # pages et widgets Qt
├── core/              # logique métier, indépendante de Qt
│   ├── presets/       # schémas Pydantic, bibliothèque, composition
│   ├── visual/        # pipeline de rendu, renderers, shaders GLSL
│   ├── vision/        # segmentation, contour, extraction de Fourier
│   ├── audio/         # synthèse, import WAV, lecteur
│   ├── report/        # sections, gabarits Jinja2, export PDF
│   └── storage/       # chemins, JSON atomique, cache
├── resources/         # icônes, polices, sons, presets par défaut, QSS
├── tests/             # pytest
├── scripts/           # build, téléchargement des modèles, icônes
└── docs/
```

Principes :

- **Séparation UI / métier.** `core/` n'importe jamais `ui/` ni `app/`. Seul `core/audio/player.py` dépend de Qt (`QMediaPlayer`).
- **Presets comme source de vérité.** Tout ce qui est affiché ou exporté se déduit d'un preset validé par Pydantic.
- **Rendu pur.** `rendre(preset, t)` est une fonction du preset et du temps, ce qui rend le rendu testable et reproductible.
- **Stockage local, écritures atomiques.** Aucun état n'est perdu en cas d'arrêt brutal.
- **Dépendances lourdes à la demande.** Les modèles PyTorch ne sont chargés qu'à la première utilisation du mode Analyse.

Plus de détails dans [`docs/architecture.md`](docs/architecture.md).

## Rapports scientifiques

Un rapport est un document autoportant : le HTML embarque ses images et ses styles, le PDF est généré à partir de ce même HTML via WeasyPrint. Il peut être archivé ou partagé sans dépendance externe.

Contenu d'un rapport :

- **Visuel** : image PNG, animation GIF, paramètres du preset, formules rendues en LaTeX.
- **Audio** : forme d'onde et spectre du drone associé.
- **Fourier** : coefficients de la décomposition, spectre d'amplitude, harmoniques dominantes.
- **Métriques** : erreur de reconstruction (RMSE) en fonction du nombre d'harmoniques retenues.
- **Reproductibilité** : preset complet, version de MathArt, graine aléatoire, date de génération.

Exemples dans [`docs/exemples/`](docs/exemples/).

## Feuille de route

**V1** : version courante en développement.
- [ ] Modes Créatif et Analyse
- [ ] Bibliothèque de presets visuels et audio
- [ ] Composition par couches et symétries
- [ ] Pomodoro et mode plein écran
- [ ] Rapports HTML et PDF
- [ ] Installeur Windows

**V1.1**
- [ ] Export vidéo (MP4) des animations
- [ ] Renderers supplémentaires (attracteurs, IFS, courbes de Bézier)
- [ ] Partage de presets sous forme d'archives `.zip`

**V2**
- [ ] Régression symbolique : retrouver une équation explicite à partir d'un contour
- [ ] Analyse de séquences vidéo
- [ ] Prise en charge de macOS et Linux

Cette feuille de route est indicative et peut évoluer.

## Contribuer

Les contributions sont les bienvenues.

1. Ouvrir une *issue* pour discuter du changement avant de commencer.
2. Créer une branche depuis `main`.
3. Respecter le style du projet : type hints, docstrings, `logging` plutôt que `print`.
4. Ajouter ou mettre à jour les tests, puis lancer `pytest`.
5. Ouvrir une *pull request* avec une description claire.

```powershell
pip install pytest ruff
pytest
ruff check .
```

## Licence

Distribué sous licence **MIT**. Voir le fichier [`LICENSE`](LICENSE).

## Remerciements


- Les travaux de Benoît Mandelbrot, Edward Lorenz et Jules Lissajous, ainsi que la littérature sur les descripteurs de Fourier elliptiques.
- Les projets open source utilisés : Qt for Python, NumPy, SciPy, OpenCV, PyTorch, Pydantic, Jinja2, WeasyPrint et Matplotlib.

