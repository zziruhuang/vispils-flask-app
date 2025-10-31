# 🚀 Quick Release Checklist

## Dependencies Updated ✅

### Files Changed:

- ✅ `requirements.txt` - Updated to Oct 2025 versions
- ✅ `conda-vispils.yml` - Python 3.11, cleaned 85%
- ✅ `runtime.txt` - Python 3.6.10 → 3.11.10

### Key Updates:

| Component        | Old    | New     | Change      |
| ---------------- | ------ | ------- | ----------- |
| **Python**       | 3.6.10 | 3.11.10 | 🔴 CRITICAL |
| **Flask**        | 2.3.3  | 3.0.3   | Major       |
| **PyTorch**      | 2.0.1  | 2.4.1   | Major       |
| **Pandas**       | 2.0.3  | 2.2.2   | Major       |
| **scikit-learn** | 1.3.0  | 1.5.1   | Major       |

---

## Pre-Release Testing

```bash
# 1. Install dependencies
conda env create -f conda-vispils.yml
conda activate vispils

# 2. Run tests
pytest tests/

# 3. Test the app
python app/app.py

# 4. Verify key functionality
curl http://localhost:5000/  # Should return 200

# 5. Test molecular visualization
python -c "from rdkit import Chem; print(Chem.MolFromSmiles('C'))"

# 6. Test ML model loading
python -c "import torch; print(torch.cuda.is_available())"
```

---

## Deployment Options

### Option 1: Heroku (recommended with Procfile)

```bash
git push heroku main
# Automatically uses runtime.txt (Python 3.11)
```

### Option 2: Docker

```dockerfile
FROM python:3.11-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "app.app:app"]
```

### Option 3: Manual Server

```bash
conda env create -f conda-vispils.yml
conda activate vispils
gunicorn --workers 4 --bind 0.0.0.0:5000 'app.app:app'
```

---

## Rollback Plan

If issues arise:

```bash
# Revert all changes
git checkout HEAD -- requirements.txt conda-vispils.yml runtime.txt

# Or recreate old environment
conda env create -f conda-backup-20250704/myenv_backup.yml
```

---

## Breaking Changes to Monitor

1. **Python 3.6 → 3.11:**

   - String formatting (use f-strings)
   - Type hints (modern syntax)
   - Removed modules (check imports)

2. **Flask 2.3 → 3.0:**

   - JSON encoding changes
   - AsyncIO requirements
   - Deprecation warnings

3. **Performance:**
   - Code may run 10-60% faster
   - Watch for timing-sensitive code

---

## Documentation

See `DEPENDENCY_UPDATE_REPORT.md` for:

- Detailed changelog
- All package versions
- Migration notes
- Troubleshooting guide

---

**Status:** Ready to release ✅  
**Last Updated:** Oct 31, 2025
