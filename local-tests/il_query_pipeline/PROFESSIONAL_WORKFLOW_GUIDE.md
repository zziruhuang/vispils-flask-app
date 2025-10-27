# Professional IL Viscosity Prediction Workflow

- Read: 20-min
- Purpose: Complete reference

## Overview

You've developed a **robust, production-ready pipeline** for querying ionic liquid (IL) data and generating viscosity predictions using trained Graph Convolutional Neural Networks (GCNNs). This document consolidates the workflow and best practices for your future professional use.

## 🎯 Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  INPUT: Cation + Anion SMILES                               │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│  DATA LOADING & SANITIZATION (data_utils.py)                │
│  - Load VISPILS experimental dataset                        │
│  - Standardize column names                                 │
│  - Query for specific IL                                    │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│  INPUT PREPARATION (chemprop_utils.py)                      │
│  - Create SMILES CSV                                        │
│  - Create descriptors CSV                                   │
│  - Generate input files for GCNN                            │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│  MODEL PREDICTION (chemprop_utils.py)                       │
│  - Run trained GCNN on predictions                          │
│  - Parse output predictions                                 │
│  - Convert to viscosity values                              │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│  COMPARISON & ANALYSIS (data_utils.py + analysis)           │
│  - Merge experimental + predicted (tolerance matching)      │
│  - Calculate error metrics (MAE, RMSE, % error)            │
│  - Statistical analysis                                     │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│  VISUALIZATION & REPORTING                                  │
│  - Viscosity vs temperature plots                           │
│  - Parity plots (exp vs pred)                               │
│  - Error distribution analysis                              │
│  - Export CSV + figures                                     │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│  OUTPUT: Results, Figures, Summary Reports                  │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Core Components

### 1. **Module: `il_prediction_pipeline.py`** (NEW)

- **Class:** `ILViscosityPipeline`
- **Purpose:** Single entry point for the complete workflow
- **Key Methods:**
  - `load_experimental_data()` - Load VISPILS database
  - `set_il_from_smiles()` - Define ionic liquid
  - `query_il()` - Query experimental data
  - `create_prediction_inputs()` - Prepare GCNN inputs
  - `run_prediction()` - Execute model
  - `load_and_compare()` - Compare with experimental data
  - `get_error_summary()` - Error statistics
  - `create_visualizations()` - Generate figures
  - `run_full_workflow()` - Execute complete pipeline

### 2. **Module: `data_utils.py`** (Enhanced)

- `merge_with_tolerance()` - Fuzzy temperature matching
- `rename_cols_df()` - Standardize column names
- `dfUtils` class - DataFrame utilities

### 3. **Module: `chemprop_utils.py`** (Enhanced)

- `create_chemprop_input_files()` - Prepare inputs
- `run_chemprop_prediction()` - Execute model
- `process_chemprop_results()` - Parse results
- `to_display_path()` - Path display utility

### 4. **Notebook: `IL_Viscosity_Pipeline_Professional.ipynb`** (NEW)

- Clean, consolidated template
- 8-step workflow (setup → results export)
- Clear section markers and documentation
- Production-ready code

## 🚀 Quick Start Guide

### Option A: Using the Professional Template Notebook

```python
# Simply follow the 8 sections:
# 1. Import libraries
# 2. Define cation + anion SMILES
# 3. Query experimental data
# 4. Create prediction inputs
# 5. Run predictions (dry-run → actual)
# 6. Load and compare results
# 7. Create visualizations
# 8. Export results
```

### Option B: Using the Pipeline Class

```python
from il_prediction_pipeline import ILViscosityPipeline

# Initialize pipeline
pipeline = ILViscosityPipeline(
    data_path="../../vispils/data/data_vispils.csv",
    model_checkpoint_path="../../vispils/models/model-corr-5-temp-100-3-2-scale3-constrain-seed42",
    predict_script_path="../../vispils/predict.py",
    temperature_tolerance=1.0,  # K
    output_dir="./pipeline_output",
    verbose=True
)

# Run complete workflow
results = pipeline.run_full_workflow(
    cation_smiles="CCCCn1cc[n+](C)c1",
    anion_smiles="F[B-](F)(F)F",
    dry_run=False  # Set to True for preview
)

# Access results
print(f"MAE: {results['error_metrics']['mae']:.4f}")
print(f"Results file: {results['results_file']}")
print(f"Figures: {results['figures']}")
```

## 🔑 Key Features

### 1. **Robust Temperature Matching**

- Handles temperature precision differences
- Configurable tolerance (default: 1.0 K)
- No data loss from mismatches

```python
# Example: 273.15 K matches with 273 K when tolerance=1.0
df_merged = merge_with_tolerance(
    df_exp, df_pred,
    tolerance=1.0
)
```

### 2. **Comprehensive Error Analysis**

- MAE (Mean Absolute Error)
- RMSE (Root Mean Square Error)
- Max error tracking
- Percent error calculation

### 3. **Professional Visualizations**

- **Figure 1:** 4-subplot comprehensive analysis
- **Figure 2:** Simplified 2-subplot view
- All figures at 300 DPI for publication quality

### 4. **Modular Design**

- Each component independently reusable
- Easy to extend or customize
- Clear separation of concerns

## 📊 Output Structure

```
./pipeline_output/
├── viscosity_analysis.png          # 4-subplot analysis
├── viscosity_parity.png            # Simplified parity view
├── viscosity_comparison.csv        # Detailed results table
└── prediction_summary.txt          # Summary statistics
```

## 🎨 Customization Guide

### Change Temperature Range

```python
# In notebook Section 4:
target_temperature_k = [280, 290, 300, 310, 320]  # Custom range
```

### Adjust Visualization Styles

```python
# In notebook Section 7:
subset_styles = {
    'Experimental': {'marker': 'o', 'color': 'blue', ...},
    'Predicted': {'marker': '^', 'color': 'red', ...}
}
```

### Use Different Model

```python
pipeline = ILViscosityPipeline(
    model_checkpoint_path="/path/to/your/model"
)
```

### Modify Output Directory

```python
pipeline = ILViscosityPipeline(
    output_dir="./my_custom_output"
)
```

## 💡 Best Practices

### 1. **Always Use Dry-Run First**

```python
# Verify command before execution
pipeline.run_prediction(dry_run=True)
```

### 2. **Validate SMILES Strings**

- Check molecular structure visualization
- Ensure charges are correct
- Use online tools for verification

### 3. **Check Data Availability**

```python
# Query returns data for IL
df_query = pipeline.query_il()
assert len(df_query) > 0, "No data found for IL"
```

### 4. **Review Error Metrics**

- MAE < 0.2 log units: Excellent prediction
- MAE 0.2-0.3 log units: Good prediction
- MAE > 0.3 log units: Verify data quality

### 5. **Save All Results**

```python
pipeline.save_results()
pipeline.create_visualizations()
```

## 🔧 Troubleshooting

| Issue                        | Solution                                                       |
| ---------------------------- | -------------------------------------------------------------- |
| No data found for IL         | Check SMILES string sanitization; verify IL exists in database |
| Missing temperature_k column | Use `merge_with_tolerance()` with correct column names         |
| Prediction takes too long    | Check model size; may need GPU acceleration                    |
| Figures not displaying       | Ensure matplotlib backend is set to interactive                |
| CSV export fails             | Check write permissions in output directory                    |

## 📚 File Organization

```
vispils-flask-app/local-tests/
├── scripts/
│   ├── il_prediction_pipeline.py      ← Main pipeline class (NEW)
│   ├── data_utils.py                  ← Data utilities
│   ├── chemprop_utils.py              ← GCNN utilities
│   └── smiles_utils.py                ← SMILES handling
├── ipynb-notebooks/
│   ├── 251018_process_quered_jl.ipynb ← Original development notebook
│   └── IL_Viscosity_Pipeline_Professional.ipynb  ← New template (NEW)
└── results/
    ├── viscosity_comparison.csv
    ├── prediction_summary.txt
    └── figures/
        ├── viscosity_analysis.png
        └── viscosity_parity.png
```

## 🚦 Workflow Decision Tree

```
START
  ↓
Need quick analysis?
  ├─ YES → Use Professional Notebook
  └─ NO → Use Pipeline Class
  ↓
Define IL (cation + anion SMILES)
  ↓
Load data → Query IL → Check availability
  ↓
Prepare inputs → Create CSVs
  ↓
Dry-run? → Verify command
  ↓
Execute prediction
  ↓
Load + merge results
  ↓
Analyze errors
  ↓
Create visualizations
  ↓
Export to CSV + save figures
  ↓
Review summary report
  ↓
END ✓
```

## 📈 Scalability Considerations

### For Multiple ILs:

```python
ils = [
    ("CCCCn1cc[n+](C)c1", "F[B-](F)(F)F"),  # IL 1
    ("CCCCn1cc[n+](C)c1", "C(F)(F)F[B-]"),  # IL 2
]

for cation, anion in ils:
    results = pipeline.run_full_workflow(cation, anion, dry_run=False)
    # Process results...
```

### For Batch Processing:

- Use the `ILViscosityPipeline` class
- Implement caching of experimental data
- Parallelize predictions if possible
- Generate consolidated comparison tables

## 🎯 Next Steps

1. **Validate** the pipeline with additional ILs
2. **Benchmark** model performance across temperature ranges
3. **Integrate** into automated analysis workflow
4. **Document** model selection criteria
5. **Create** publication-ready figures
6. **Archive** results with metadata

## 📝 Citation & References

If you use this pipeline for research:

- Cite the VISPILS dataset
- Reference GCNN model paper
- Document your IL selection criteria
- Include error metrics in results

## 🤝 Contributing & Extending

To extend the pipeline:

1. Add new error metrics to `get_error_summary()`
2. Implement additional visualizations
3. Create reporting templates
4. Add batch processing capabilities
5. Develop parameter optimization functions

---

**Created:** October 2025  
**Author:** Ziru Huang  
**Status:** Production-Ready ✓
