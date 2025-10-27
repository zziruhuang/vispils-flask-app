# Technical Appendix: VISPILS vs. CMPNN/Chemprop

This appendix provides a detailed, file-by-file and function-by-function summary of the key VISPILS-specific extensions and innovations over the original CMPNN/Chemprop frameworks, with a focus on correlation descriptors and ionic liquid (IL) property prediction.

---

## 1. Correlation Descriptors: The Core VISPILS Innovation

### `vispils/chemprop/features/correlations.py`

- **Purpose:** Implements atomic correlation descriptors, the key difference from original CMPNN/Chemprop.
- **Key Functions:**
  - `atomic_correlations(smiles, CORR_FEATURES, CORR_SCALES, max_length=66)`: Computes pairwise atomic property correlations between cation and anion for a given IL SMILES.
  - `get_corr_scale_scheme(scheme)`: Defines scaling for each correlation descriptor.
  - `CORR_FEATURES` dict: Maps descriptor names to atomic property functions (e.g., volume, polarisability, electron affinity).
- **Integration:** Used in featurization to provide IL-specific, physically meaningful features for ML.

### `vispils/chemprop/features/atomfeatures.py`

- **Purpose:** Defines atomic property functions used in correlation descriptors (e.g., `atomic_volume`, `atomic_polarisability`, `electron_affinity`, etc.).
- **Integration:** Imported and used by `correlations.py` and featurization logic.

---

## 2. Feature Extraction and Featurization

### `vispils/chemprop/features/featurization.py`

- **Purpose:** Central featurization logic for molecules, extended to include correlation descriptors.
- **Key Extensions:**
  - `CORR_FEATURES, CORR_SCALES = pass_corr_scheme()`: Loads correlation descriptor functions and scaling.
  - `CORR_DIM` and `ATOM_FDIM`: Feature vector dimensionality now includes correlation descriptor dimensions.
  - `MolGraph.__init__`: Calls `atomic_correlations` to compute and store correlation features for each molecule.
  - `atom_features_new`: Extended atom feature vector to include correlation descriptors and IL-specific properties.

### `vispils/chemprop/features/features_generators.py`

- **Purpose:** Registry and implementation of feature generators (e.g., Morgan, RDKit 2D, custom). Can be extended to register IL-specific or correlation-based generators.

---

## 3. Data Handling and Prediction Pipeline

### `vispils/chemprop/data/data.py`

- **Purpose:** Data loading and dataset management, supports additional features (including correlation descriptors) for each molecule.
- **Key Extensions:**
  - `MoleculeDatapoint.__init__`: Loads and attaches custom features to each molecule.
  - `MoleculeDataset.features()`: Returns feature arrays, including correlation descriptors.

### `vispils/predict.py`

- **Purpose:** Main prediction script for batch and single-molecule inference.
- **Key Extensions:**
  - Loads both SMILES and feature CSVs (including correlation descriptors) and concatenates them for prediction.
  - Calls Chemprop/CMPNN model for property prediction.

---

## 4. Model Training and Inference

### `vispils/chemprop/train/predict.py`

- **Purpose:** Batch prediction logic for model ensembles.
- **Integration:** Accepts feature arrays (including correlation descriptors) for inference.

---

## 5. Integration with VISPILS Web Platform

- **Flask API:** The backend wraps the prediction pipeline, exposing it as a RESTful API for real-time web use.
- **Frontend:** The web UI and JSmol viewer are tightly integrated with the backend, enabling seamless user experience from input to 3D visualization.

---

## Summary Table: VISPILS-Specific Files and Functions

| File/Module                       | VISPILS-Specific Role/Extension                         |
| --------------------------------- | ------------------------------------------------------- |
| `features/correlations.py`        | Implements correlation descriptors for ILs              |
| `features/atomfeatures.py`        | Defines atomic property functions for correlations      |
| `features/featurization.py`       | Integrates correlation descriptors into feature vectors |
| `features/features_generators.py` | Registry for custom/IL-specific feature generators      |
| `chemprop/data/data.py`           | Loads and attaches custom features to molecules         |
| `predict.py`                      | Loads features, runs model prediction, outputs results  |
| `chemprop/train/predict.py`       | Batch prediction with feature arrays                    |
| (Flask backend, not shown here)   | Wraps model for web API use                             |

---

**This appendix documents the technical innovations that make VISPILS uniquely suited for ionic liquid property prediction, with a focus on correlation descriptors and IL-specific data handling.**
