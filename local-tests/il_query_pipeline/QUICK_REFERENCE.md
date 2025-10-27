# IL Viscosity Pipeline - Quick Reference

## 🎬 Fastest Way to Get Started: Python Module

```python
# Step 1: Import and initialize
from il_prediction_pipeline import ILViscosityPipeline

pipeline = ILViscosityPipeline(verbose=True)

# Step 2: Define your ionic liquid
cation = "CCCCn1cc[n+](C)c1"  # 1-Butyl-3-methylimidazolium
anion = "F[B-](F)(F)F"         # Tetrafluoroborate

# Step 3: Run everything (with dry-run preview first)
results_preview = pipeline.run_full_workflow(cation, anion, dry_run=True)
print("✓ Dry run successful. Command verified.")

# Step 4: Execute actual predictions
results = pipeline.run_full_workflow(cation, anion, dry_run=False)

# Step 5: Access your results
print(f"MAE: {results['error_metrics']['mae']:.4f} log units")
print(f"Files saved to: {results['results_file']}")
```

## 📋 Notebook Path (Easiest)

Simply open and follow: **`IL_Viscosity_Pipeline_Professional.ipynb`**

Each section is numbered 1-8. Just run them in order.

## 🔧 Common Tasks

### Change Temperature Range

```python
# In pipeline.run_full_workflow():
results = pipeline.run_full_workflow(
    cation, anion,
    temperatures=[280, 290, 300, 310, 320]
)
```

### Use Different Model

```python
pipeline = ILViscosityPipeline(
    model_checkpoint_path="/path/to/your/model"
)
```

### Adjust Temperature Tolerance

```python
pipeline = ILViscosityPipeline(
    temperature_tolerance=0.5  # stricter matching
)
```

### Silent Mode (No Output)

```python
pipeline = ILViscosityPipeline(verbose=False)
```

## 📊 Understanding Results

### Error Metrics

| Metric | Range     | Interpretation |
| ------ | --------- | -------------- |
| MAE    | 0.0-0.15  | Excellent      |
| MAE    | 0.15-0.25 | Very good      |
| MAE    | 0.25-0.35 | Good           |
| MAE    | > 0.35    | Check data     |

**Example:**

```python
error_summary = pipeline.get_error_summary()
mae = error_summary['mae']
rmse = error_summary['rmse']
```

### Output Files

- `viscosity_analysis.png` - 4 subplots: trends + parity + errors
- `viscosity_parity.png` - Simple 2-plot version
- `viscosity_comparison.csv` - Raw data table
- `prediction_summary.txt` - Text report

## 🚨 Troubleshooting Quick Fixes

### ❌ "No data found for IL"

```python
# Check SMILES sanitization
from smiles_utils import sanitized_smiles
print(sanitized_smiles("CCCCn1cc[n+](C)c1.F[B-](F)(F)F"))
```

### ❌ "Temperature columns missing"

```python
# Use merge_with_tolerance with correct names
from data_utils import merge_with_tolerance
df_merged = merge_with_tolerance(
    df_exp, df_pred,
    left_key='temperature_k',
    right_key='temperature_k',
    tolerance=1.0
)
```

### ❌ "Prediction times out"

```python
# Pre-view command with dry-run=True
results = pipeline.run_prediction(dry_run=True)
# Check if script path is correct
```

### ❌ "Can't save figures"

```python
# Ensure directory exists
from pathlib import Path
Path("./figures").mkdir(exist_ok=True)
```

## 💾 Saving Your Work

```python
# Everything is saved automatically:
pipeline.save_results()  # → ../results/viscosity_comparison.csv
pipeline.create_visualizations()  # → ./figures/*.png

# Custom save location:
pipeline.output_dir = Path("./my_results")
pipeline.save_results("custom_name.csv")
```

## 📈 Processing Multiple ILs

```python
ils = [
    ("CCCCn1cc[n+](C)c1", "F[B-](F)(F)F"),
    ("CCCCN(CC)CC", "C(C)(C)C[B-](F)(F)F"),
]

for cation, anion in ils:
    print(f"Processing: {cation}.{anion}")
    results = pipeline.run_full_workflow(cation, anion, dry_run=False)
    print(f"  MAE: {results['error_metrics']['mae']:.4f}\n")
```

## 🎨 Customizing Plots

In the notebook, modify this section:

```python
subset_styles = {
    'Experimental': {
        'marker': 'o',      # ← change to '^', 's', etc.
        'color': 'blue',    # ← any matplotlib color
        'label': 'Exp',
        's': 100,           # ← size
        'alpha': 0.7,       # ← transparency
    },
    'Predicted': {
        'marker': '^',
        'color': 'red',
        'label': 'Pred',
        's': 100,
        'alpha': 0.7,
    }
}
```

## 🔗 File Locations

```
Your Workspace:
├── scripts/
│   ├── il_prediction_pipeline.py  ← Pipeline class
│   ├── data_utils.py              ← Utilities
│   ├── chemprop_utils.py          ← GCNN interface
│   └── smiles_utils.py            ← SMILES handling
├── ipynb-notebooks/
│   ├── IL_Viscosity_Pipeline_Professional.ipynb  ← Use this!
│   └── 251018_process_quered_jl.ipynb            ← Reference
└── Data & Models:
    ├── ../../vispils/data/data_vispils.csv       ← Experimental data
    ├── ../../vispils/predict.py                  ← Prediction script
    └── ../../vispils/models/model-...            ← Trained model
```

## ⚡ Performance Tips

1. **Use dry-run first** (5 seconds) before full run
2. **Batch multiple ILs** to avoid data reloading
3. **Save intermediate results** during long workflows
4. **Use verbose=False** to reduce output overhead
5. **Pre-filter temperature** if only interested in range

## 📞 When Things Go Wrong

### Check 1: Verify Paths

```python
from pathlib import Path
Path("../../vispils/data/data_vispils.csv").exists()  # Should be True
```

### Check 2: Verify Data

```python
df = pipeline.load_experimental_data()
print(f"Loaded {len(df)} rows")
print(f"Columns: {df.columns.tolist()}")
```

### Check 3: Verify IL Query

```python
df_query = pipeline.query_il()
print(f"Found {len(df_query)} records for IL")
```

### Check 4: Check Model

```python
import subprocess
result = subprocess.run(
    ["python", "../../vispils/predict.py", "--help"],
    capture_output=True
)
print(result.stdout.decode())
```

## 🎯 Example Workflows

### Quick Check (5 min)

```python
pipeline.run_full_workflow(cation, anion, dry_run=True)
```

### Full Analysis (30 min)

```python
pipeline.run_full_workflow(cation, anion, dry_run=False)
```

### Batch Processing (1-2 hours)

```python
for cation, anion in il_list:
    pipeline.run_full_workflow(cation, anion, dry_run=False)
```

### Parameter Sweep (multiple models)

```python
models = ["model1", "model2", "model3"]
for model in models:
    pipeline.model_checkpoint_path = Path(f"../../vispils/models/{model}")
    pipeline.run_full_workflow(cation, anion, dry_run=False)
```

## 📝 Export Results

```python
# CSV table of results
df_comparison.to_csv("results.csv", index=False)

# Publication-ready figures (already 300 DPI)
# - ./figures/viscosity_analysis.png
# - ./figures/viscosity_parity.png

# Summary statistics
error_summary = pipeline.get_error_summary()
for key, value in error_summary.items():
    print(f"{key}: {value}")
```

## 🚀 You're Ready!

**→ Open:** `IL_Viscosity_Pipeline_Professional.ipynb`

**→ Run:** Each section in order (1-8)

**→ Get:** Analysis, figures, and CSV results

**✓ Done!**

---

For detailed documentation, see: `PROFESSIONAL_WORKFLOW_GUIDE.md`
