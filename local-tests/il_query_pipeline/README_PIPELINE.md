# 🔬 IL Viscosity Prediction Pipeline - Complete Documentation Index

## 📋 Start Here

**New to this pipeline?** Start with one of these:

1. **[⚡ QUICK_REFERENCE.md](./QUICK_REFERENCE.md)** (5 min read)

   - Copy-paste examples
   - Common tasks
   - Quick troubleshooting

2. **[📚 PROFESSIONAL_WORKFLOW_GUIDE.md](./PROFESSIONAL_WORKFLOW_GUIDE.md)** (20 min read)

   - Complete architecture
   - Best practices
   - Customization guide
   - Scalability tips

3. **[🎯 CONSOLIDATION_SUMMARY.md](./CONSOLIDATION_SUMMARY.md)** (10 min read)
   - What you've built
   - How to use going forward
   - Success metrics
   - Next steps

---

## 📚 Documentation Library

### Getting Started

| Document                                                           | Time   | Purpose                  |
| ------------------------------------------------------------------ | ------ | ------------------------ |
| [QUICK_REFERENCE.md](./QUICK_REFERENCE.md)                         | 5 min  | Fast setup & examples    |
| [CONSOLIDATION_SUMMARY.md](./CONSOLIDATION_SUMMARY.md)             | 10 min | Overview & next steps    |
| [PROFESSIONAL_WORKFLOW_GUIDE.md](./PROFESSIONAL_WORKFLOW_GUIDE.md) | 20 min | Deep dive & architecture |

### Technical Guides

| Document                                                                                           | Topic                 | Purpose                      |
| -------------------------------------------------------------------------------------------------- | --------------------- | ---------------------------- |
| [TEMPERATURE_MATCHING_GUIDE.md](./TEMPERATURE_MATCHING_GUIDE.md)                                   | Temperature tolerance | Understanding fuzzy matching |
| [PROFESSIONAL_WORKFLOW_GUIDE.md#troubleshooting](./PROFESSIONAL_WORKFLOW_GUIDE.md#troubleshooting) | Troubleshooting       | Fix common issues            |
| [PROFESSIONAL_WORKFLOW_GUIDE.md#customization](./PROFESSIONAL_WORKFLOW_GUIDE.md#customization)     | Customization         | Modify for your needs        |

---

## 🚀 Quick Start Paths

### Path A: Notebook User (Easiest)

```
1. Open: IL_Viscosity_Pipeline_Professional.ipynb
2. Follow: 8 sections in order
3. Get: Predictions, error metrics, figures
Time: ~30 minutes
```

### Path B: Python Developer

```python
from scripts.il_prediction_pipeline import ILViscosityPipeline

pipeline = ILViscosityPipeline()
results = pipeline.run_full_workflow("cation", "anion", dry_run=False)
```

See [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) for details

### Path C: Batch Processing

```python
# Process multiple ILs
for cation, anion in il_list:
    pipeline.run_full_workflow(cation, anion, dry_run=False)
```

See [PROFESSIONAL_WORKFLOW_GUIDE.md](./PROFESSIONAL_WORKFLOW_GUIDE.md#scalability)

---

## 📂 Key Files

### Code (Scripts)

- **`scripts/il_prediction_pipeline.py`** ← Main pipeline class
- **`scripts/data_utils.py`** ← Data utilities (enhanced)
- **`scripts/chemprop_utils.py`** ← GCNN interface (enhanced)
- **`scripts/smiles_utils.py`** ← SMILES handling

### Notebooks

- **`ipynb-notebooks/IL_Viscosity_Pipeline_Professional.ipynb`** ← Use this!
- **`ipynb-notebooks/251018_process_quered_jl.ipynb`** ← Reference

### Documentation

- **`QUICK_REFERENCE.md`** ← Start here for quick setup
- **`PROFESSIONAL_WORKFLOW_GUIDE.md`** ← Complete guide
- **`CONSOLIDATION_SUMMARY.md`** ← Overview & next steps
- **`TEMPERATURE_MATCHING_GUIDE.md`** ← Temperature tolerance explained

### Outputs (Generated)

- **`results/viscosity_comparison.csv`** ← Detailed results
- **`results/prediction_summary.txt`** ← Summary report
- **`figures/viscosity_analysis.png`** ← 4-subplot analysis
- **`figures/viscosity_parity.png`** ← Parity plot

---

## 🎯 What This Pipeline Does

```
INPUT: Cation SMILES + Anion SMILES
  ↓
LOAD experimental data (VISPILS database)
  ↓
QUERY data for your ionic liquid
  ↓
CREATE input files for GCNN model
  ↓
RUN predictions (trained neural network)
  ↓
COMPARE experimental vs predicted viscosity
  ↓
ANALYZE errors & generate report
  ↓
CREATE publication-quality figures
  ↓
OUTPUT: CSV results + PNG figures + summary report
```

---

## 💡 Key Features

✅ **Robust Temperature Matching**

- Handles precision differences (e.g., 273.15 K vs 273 K)
- Configurable tolerance
- No data loss

✅ **Comprehensive Error Analysis**

- MAE, RMSE, max error, percent error
- Statistical summaries
- Error distribution analysis

✅ **Professional Visualizations**

- 4-subplot comprehensive analysis
- Parity plots with error metrics
- 300 DPI publication-ready

✅ **Complete Workflow Automation**

- Single class handles everything
- Clear error messages
- Dry-run mode for safety

✅ **Scalable Design**

- Process single IL or batch
- Reusable components
- Easy to extend

---

## 🔧 Common Tasks

### I want to...

**...run a quick analysis**
→ See [QUICK_REFERENCE.md](./QUICK_REFERENCE.md)

**...process multiple ILs**
→ See [PROFESSIONAL_WORKFLOW_GUIDE.md#scalability](./PROFESSIONAL_WORKFLOW_GUIDE.md#scalability)

**...customize the plots**
→ See [QUICK_REFERENCE.md#customizing-plots](./QUICK_REFERENCE.md#customizing-plots)

**...understand temperature matching**
→ See [TEMPERATURE_MATCHING_GUIDE.md](./TEMPERATURE_MATCHING_GUIDE.md)

**...fix an error**
→ See [PROFESSIONAL_WORKFLOW_GUIDE.md#troubleshooting](./PROFESSIONAL_WORKFLOW_GUIDE.md#troubleshooting)

**...extend the pipeline**
→ See [PROFESSIONAL_WORKFLOW_GUIDE.md#contributing](./PROFESSIONAL_WORKFLOW_GUIDE.md#contributing--extending)

**...use it in production**
→ See [PROFESSIONAL_WORKFLOW_GUIDE.md#scalability](./PROFESSIONAL_WORKFLOW_GUIDE.md#scalability-considerations)

---

## 📊 Understanding Your Results

### Error Metrics

| Metric | Excellent | Good      | Fair      | Poor   |
| ------ | --------- | --------- | --------- | ------ |
| MAE    | < 0.15    | 0.15-0.25 | 0.25-0.35 | > 0.35 |
| RMSE   | < 0.2     | 0.2-0.3   | 0.3-0.4   | > 0.4  |

### Output Files

After running the pipeline, you'll get:

1. **`viscosity_comparison.csv`** - Detailed table with:
   - Temperature, experimental viscosity, predicted viscosity
   - Error (prediction - experimental)
   - Absolute error, percent error
2. **`viscosity_analysis.png`** - 4 subplots:

   - Viscosity vs temperature (linear)
   - Viscosity vs temperature (log)
   - Parity plot (experimental vs predicted)
   - Error distribution

3. **`viscosity_parity.png`** - Simplified view:

   - Log viscosity vs temperature
   - Parity plot

4. **`prediction_summary.txt`** - Text report with:
   - IL information
   - Experimental data summary
   - Prediction statistics
   - File locations

---

## 🏃 Running Right Now

### Quickest Start (5 min)

```bash
cd local-tests/ipynb-notebooks
jupyter notebook IL_Viscosity_Pipeline_Professional.ipynb
```

Then follow sections 1-8 in the notebook.

### Command Line (Python)

```python
from scripts.il_prediction_pipeline import ILViscosityPipeline

# Create pipeline
pipeline = ILViscosityPipeline(verbose=True)

# Run complete workflow
results = pipeline.run_full_workflow(
    cation_smiles="CCCCn1cc[n+](C)c1",
    anion_smiles="F[B-](F)(F)F",
    dry_run=False
)

# Access results
print(f"MAE: {results['error_metrics']['mae']:.4f}")
print(f"Files: {results['figures']}")
```

---

## 📚 Learning Resources

### Understand the Pipeline

1. Read [CONSOLIDATION_SUMMARY.md](./CONSOLIDATION_SUMMARY.md) for overview
2. See [PROFESSIONAL_WORKFLOW_GUIDE.md#pipeline-architecture](./PROFESSIONAL_WORKFLOW_GUIDE.md#pipeline-architecture)
3. Review notebook code

### Understand Temperature Matching

→ [TEMPERATURE_MATCHING_GUIDE.md](./TEMPERATURE_MATCHING_GUIDE.md)

### Understand Results

→ [PROFESSIONAL_WORKFLOW_GUIDE.md#output-structure](./PROFESSIONAL_WORKFLOW_GUIDE.md#output-structure)

### Troubleshooting

→ [QUICK_REFERENCE.md#troubleshooting](./QUICK_REFERENCE.md#troubleshooting-quick-fixes) OR [PROFESSIONAL_WORKFLOW_GUIDE.md#troubleshooting](./PROFESSIONAL_WORKFLOW_GUIDE.md#troubleshooting)

---

## 🎓 API Reference

### Main Class

```python
from scripts.il_prediction_pipeline import ILViscosityPipeline

pipeline = ILViscosityPipeline(
    data_path="../../vispils/data/data_vispils.csv",
    model_checkpoint_path="../../vispils/models/...",
    predict_script_path="../../vispils/predict.py",
    temperature_tolerance=1.0,
    output_dir="./pipeline_output",
    verbose=True
)
```

### Key Methods

```python
# Complete workflow
results = pipeline.run_full_workflow(cation, anion, dry_run=False)

# Step-by-step
pipeline.load_experimental_data()
pipeline.set_il_from_smiles(cation, anion)
pipeline.query_il()
pipeline.create_prediction_inputs()
pipeline.run_prediction(dry_run=False)
pipeline.load_and_compare()
pipeline.create_visualizations()
pipeline.save_results()

# Get metrics
errors = pipeline.get_error_summary()
```

---

## ✅ Checklist: First Time Setup

- [ ] Read [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) (5 min)
- [ ] Verify paths to data and model exist
- [ ] Open IL_Viscosity_Pipeline_Professional.ipynb
- [ ] Run Section 1: Imports
- [ ] Run Section 2: Define SMILES
- [ ] Run Sections 3-8 in order
- [ ] Check output files were created
- [ ] Review error metrics
- [ ] Examine figures

---

## 🚀 Next Steps

1. **Try it:** Run with example SMILES (provided in notebook)
2. **Validate:** Test with 5-10 different ILs
3. **Extend:** Modify for your specific needs
4. **Scale:** Process multiple ILs in batch
5. **Share:** Use for publications or presentations

---

## 📞 Help & Support

**Question Type → See:**

- How do I get started? → [QUICK_REFERENCE.md](./QUICK_REFERENCE.md)
- What does this do? → [CONSOLIDATION_SUMMARY.md](./CONSOLIDATION_SUMMARY.md)
- How does this work? → [PROFESSIONAL_WORKFLOW_GUIDE.md](./PROFESSIONAL_WORKFLOW_GUIDE.md)
- How do I... temperature matching? → [TEMPERATURE_MATCHING_GUIDE.md](./TEMPERATURE_MATCHING_GUIDE.md)
- I got an error → [QUICK_REFERENCE.md#troubleshooting](./QUICK_REFERENCE.md#troubleshooting-quick-fixes)
- I want to customize → [QUICK_REFERENCE.md#example-workflows](./QUICK_REFERENCE.md#example-workflows)

---

## 📋 Document Navigation

```
START HERE
    ↓
Choose your path:
    ├─ 5 min? → QUICK_REFERENCE.md
    ├─ 10 min? → CONSOLIDATION_SUMMARY.md
    ├─ 20 min? → PROFESSIONAL_WORKFLOW_GUIDE.md
    └─ Specific topic? → See index below
    ↓
SPECIFIC TOPICS:
    ├─ Temperature matching → TEMPERATURE_MATCHING_GUIDE.md
    ├─ Troubleshooting → PROFESSIONAL_WORKFLOW_GUIDE.md#troubleshooting
    ├─ Customization → PROFESSIONAL_WORKFLOW_GUIDE.md#customization
    ├─ Scaling → PROFESSIONAL_WORKFLOW_GUIDE.md#scalability
    └─ Examples → QUICK_REFERENCE.md
    ↓
READY TO CODE
    ├─ Use Notebook → IL_Viscosity_Pipeline_Professional.ipynb
    ├─ Use Python Class → See QUICK_REFERENCE.md
    └─ Batch Processing → See PROFESSIONAL_WORKFLOW_GUIDE.md
    ↓
SUCCESS ✓
```

---

**Last Updated:** October 2025  
**Status:** ✅ Ready for Production Use  
**Questions?** Check the relevant guide above.
