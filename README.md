# VISPILS: AI-Powered Ionic Liquid Property Platform

**VISPILS** is a research-grade web app designed to streamline ionic liquid research by integrating molecular visualization, machine learning predictions, and comprehensive database access into a single platform. It combines experimental data integration, SOTA ML models, and interactive molecular structure viewers—all in a immersive, user-friendly interface.

---

## 🚀 Quick Start

#### 1. Clone the repo

```bash
git clone https://github.com/zziruhuang/vispils-flask-app.git
cd vispils-flask-app
```

#### 2. Create a Python environment (choose one)

Option A — Conda env file (recommended)

```bash
# If conda-vispils.yml is in the project root:
conda env create -f conda-vispils.yml
# Or if the file is elsewhere:
conda env create -f /path/to/conda-vispils.yml

conda activate vispils
```

Option B — Conda manual setup

```bash
conda create -n vispils python=3.8 -y
conda activate vispils
conda install -c conda-forge rdkit openbabel -y
conda install pytorch torchvision torchaudio -c pytorch -y
pip install -r requirements.txt
```

Option C — virtualenv / pip (advanced)

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (cmd)
venv\Scripts\activate.bat

pip install --upgrade pip
pip install -r requirements.txt
```

Note: RDKit, OpenBabel and some PyTorch builds are easiest to install via conda. Prefer Option A or B if possible.

#### 3. Prepare model directory

```bash
# macOS / Linux
mkdir -p vispils/model

# Windows (cmd / PowerShell)
mkdir vispils\model
```

Place your trained model files in vispils/model/

#### 4. Run the app

```bash
conda activate vispils

python app/app.py
# Visit: http://localhost:5001

conda deactivate
```

#### Quick API test

```bash
curl -X POST http://localhost:5001/api/predict \
  -H "Content-Type: application/json" \
  -d '{"smiles":"CCO","temperature":298}'
```

#### Installation Notes

**Important:** The current repo uses `.gitkeep` placeholder files to preserve directory structure for large assets that are not tracked by Git:

- **`frontend/static/jsmol/`** – JSmol third-party package (download from [JSmol](http://wiki.jmol.org/index.php/JSmol))
- **`frontend/static/img/`** – Frontend images (.png, .jpg, etc.)
- **`app/data/`** – Application data files (.csv, .mol, etc.)
- **`vispils/data/`** – Training/validation data (.csv, .xlsx, etc.)
- **`vispils/models/`** – Trained ML model files (.pt, .pth, etc.)

These directories contain `.gitkeep` files only. You must populate them with the actual assets before running the app. Large files will be managed via Git LFS or external storage in future releases.

## ✨ Features

- **Stepwise IL Builder:**
  Select cation/anion families, visualize candidates, and build custom ILs.
- **Quick Prediction:**
  Paste any SMILES and temperature, get instant ML-powered property predictions.
- **Unified Results Panel:**
  See experimental and predicted values, error, and molecular structure in one place.
- **3D Molecular Viewer:**
  Explore ILs in interactive 3D with JSmol.
- **Robust Backend:**
  Flask API, Chemprop ML, RDKit/OpenBabel for chemistry, and error-tolerant workflows.
- **Modern UI:**
  Responsive, accessible, and visually appealing.

---

## 🔧 Tech Stack

- **Backend:** Flask, PyTorch, RDKit, OpenBabel
- **Frontend:** HTML5, CSS3, JavaScript, JSmol
- **ML:** Chemprop GCNN, Scikit-learn
- **Data:** ILThermo, curated sources

---

## 📚 References

- [Chemprop](https://github.com/chemprop/chemprop)
- [CMPNN](https://github.com/SY575/CMPNN)
- [ILThermo](https://ilthermo.boulder.nist.gov/)
- [RDKit](https://www.rdkit.org/)
- [JSmol](http://wiki.jmol.org/index.php/JSmol)

---

## 📜 License

MIT

---

**Ready to explore the future of ionic liquid research? Clone, run, and discover!**

```

```
