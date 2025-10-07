# VISPILS Model Module

This directory contains the machine learning code and utilities for property prediction in the VISPILS platform. The core model is based on the Communicative Message Passing Neural Network (CMPNN), originally published in [IJCAI 2020](https://www.ijcai.org/Proceedings/2020/0392.pdf) and built on top of [Chemprop](https://github.com/chemprop/chemprop).

---

## 🛠️ VISPILS Extensions and Innovations

VISPILS extends the original CMPNN/Chemprop frameworks with several domain-specific and technical innovations, making it uniquely suited for ionic liquid (IL) property prediction:

### 1. Domain-Specific Adaptation for Ionic Liquids (ILs)

- **Custom Feature Engineering:**
  - Extended the input pipeline to support IL-specific features, including temperature, cation/anion descriptors, and especially **correlation descriptors** (the key difference from the original models).
  - Developed scripts for automated feature extraction and normalization tailored to IL datasets.
- **Dataset Curation:**
  - Integrated and preprocessed data from ILThermo and other sources, ensuring compatibility with the model and enabling robust cross-validation.

### 2. End-to-End Web Integration

- **Flask API Wrapping:**
  - Refactored the prediction pipeline to be callable as a RESTful API, enabling real-time property prediction from web or programmatic clients.
  - Implemented robust error handling, logging, and input validation for production use.
- **Frontend-Backend Communication:**
  - Designed a unified API for both batch and single-molecule prediction, supporting both stepwise IL builder and quick prediction workflows.

### 3. Automated 3D Structure Generation and Visualization

- **On-the-Fly 3D Generation:**
  - Integrated OpenBabel and RDKit to generate 3D molecular structures from user-submitted SMILES strings.
  - Automated the conversion of model input/output to 3D molfile format for visualization.
- **Interactive Visualization:**
  - Connected backend predictions to a JSmol-powered frontend, allowing users to interactively explore predicted or experimental IL structures in 3D.

### 4. User Experience and Accessibility

- **Modern Web UI:**
  - Developed a responsive, accessible frontend with clear user feedback, unified results panels, and seamless integration of experimental and predicted data.
  - Provided "quick prediction" and "stepwise builder" modes to accommodate both expert and novice users.
- **Unified Results Display:**
  - Designed a results panel that presents experimental values, ML predictions, and error metrics in a single, easy-to-interpret table.

### 5. Reproducibility and Extensibility

- **Automated Data Flow:**
  - Automated the entire workflow from user input to prediction and visualization, reducing manual intervention and potential for error.
- **Documentation and Deployment:**
  - Created comprehensive documentation, including installation, usage, and developer guides.
  - Provided ready-to-use scripts and configuration files for both local and cloud deployment.

### 6. Scientific and Technical Impact

- **Bridging ML and Chemistry:**
  - Lowered the barrier for chemists and materials scientists to apply state-of-the-art ML models to IL property prediction.
- **Open Science:**
  - Built on open-source foundations ([Chemprop](https://github.com/chemprop/chemprop), [CMPNN](https://github.com/SY575/CMPNN)), and contributed new code, documentation, and workflows back to the community.

---

## 📦 Contents

- `models/` — Model architectures (CMPNN, MPNN, etc.)
- `features/` — Feature extraction scripts and data
- `train/` — Training, evaluation, and cross-validation scripts
- `predict.py` — Command-line prediction utility
- `data/` — Example datasets and feature files

---

## 🚀 How VISPILS Uses This Code

- **Training:** Models are trained on curated ionic liquid property datasets using the scripts in `train/`.
- **Prediction:** The VISPILS backend calls `predict.py` to generate property predictions for user-submitted SMILES and conditions.
- **Integration:** The model is wrapped by the Flask API, enabling real-time ML predictions in the web app.

---

## 🛠️ Usage

### Train a Model

```bash
python train/train.py --data_path <data.csv> --dataset_type regression --num_folds 5 --gpu 0 --epochs 30
```

### Predict Properties

```bash
python predict.py --data_path <input.csv> --checkpoint_dir <model_dir>
```

- `<input.csv>`: CSV with SMILES and features (see examples in `data/`)
- `<model_dir>`: Directory containing trained model checkpoints

---

## 📚 Dependencies

- Python 3.8+
- torch >= 1.2.0
- RDKit
- OpenBabel
- numpy, pandas, scikit-learn

> **Tip:** Use `conda install -c conda-forge rdkit openbabel` for chemistry packages.

---

## 🙏 Acknowledgements

- CMPNN code: [IJCAI 2020 paper](https://www.ijcai.org/Proceedings/2020/0392.pdf) by Song et al.
- Built on [Chemprop](https://github.com/chemprop/chemprop) by Yang et al.

---

## 📜 Citation

If you use this code or the VISPILS platform in your work, please cite:

```bibtex
@inproceedings{ijcai2020-392,
  title     = {Communicative Representation Learning on Attributed Molecular Graphs},
  author    = {Song, Ying and Zheng, Shuangjia and Niu, Zhangming and Fu, Zhang-hua and Lu, Yutong and Yang, Yuedong},
  booktitle = {Proceedings of the Twenty-Ninth International Joint Conference on Artificial Intelligence, {IJCAI-20}},
  publisher = {International Joint Conferences on Artificial Intelligence Organization},
  editor    = {Christian Bessiere}
  pages     = {2831--2838},
  year      = {2020},
  month     = {7},
  note      = {Main track}
  doi       = {10.24963/ijcai.2020/392},
  url       = {https://doi.org/10.24963/ijcai.2020/392},
}
```

---

## 📑 Technical Appendix: VISPILS vs. CMPNN/Chemprop

_This section will provide a file-by-file and function-by-function summary of VISPILS-specific extensions, with a focus on correlation descriptors and IL-specific data handling. (To be completed next.)_

---

**This directory is maintained and extended for the VISPILS project. For original CMPNN usage, see the original authors' documentation.**
