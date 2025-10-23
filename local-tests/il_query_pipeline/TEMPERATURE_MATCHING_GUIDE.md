# Temperature Matching with Tolerance

- Read: 10 min
- Purpose: Technical details

## Problem

When comparing experimental and predicted viscosity data, temperature values often don't match exactly due to:

- **Different precision**: Experimental: 273.15 K vs Predicted: 273 K
- **Rounding conventions**: Calculated vs measured values
- **Data source differences**: Different instruments/computational methods

For example:

```
Experimental temperatures: [273.15, 283.15, 298.15, 308.15, ...]
Predicted temperatures:    [273,    283,    298,    308,    ...]
```

A strict equality merge would fail to match any rows!

## Solution: Tolerance-Based Merging

The `merge_with_tolerance()` function in `data_utils.py` handles this by allowing a **fuzzy match** based on a tolerance range.

### Basic Usage

```python
from data_utils import merge_with_tolerance

# Merge with 1 K tolerance
df_merged = merge_with_tolerance(
    df_left=df_experimental,
    df_right=df_predicted,
    left_key='temperature_k',
    right_key='temperature_k',
    tolerance=1.0,  # Match if |temp_exp - temp_pred| <= 1.0
    how='left'
)
```

### Parameters

| Parameter   | Type      | Default           | Description                                      |
| ----------- | --------- | ----------------- | ------------------------------------------------ |
| `df_left`   | DataFrame | -                 | Left dataframe to merge from                     |
| `df_right`  | DataFrame | -                 | Right dataframe to merge from                    |
| `left_key`  | str       | `'temperature_k'` | Column name in df_left for matching              |
| `right_key` | str       | `'temperature_k'` | Column name in df_right for matching             |
| `tolerance` | float     | `1.0`             | Tolerance range for matching                     |
| `how`       | str       | `'left'`          | Type of merge: 'left', 'right', 'inner', 'outer' |

### How It Works

For each temperature in the left dataframe, the function finds **all** temperatures in the right dataframe within the tolerance range:

```
If tolerance = 1.0:
  Left temp 273.15 matches with right temps: 272.15 to 274.15
  Left temp 283.15 matches with right temps: 282.15 to 284.15
  Left temp 298.15 matches with right temps: 297.15 to 299.15
```

## Example Usage in Notebook

In the analysis cell, the function is used as:

```python
# Define tolerance
TEMPERATURE_TOLERANCE_K = 1.0

# Merge experimental and predicted data
df_comparison = merge_with_tolerance(
    df_left=df_experimental,
    df_right=df_predicted,
    left_key='temperature_k',
    right_key='temperature_k',
    tolerance=TEMPERATURE_TOLERANCE_K,
    how='left'
)

# Now you can calculate errors
df_comparison['error'] = df_comparison['predicted'] - df_comparison['experimental']
```

## Adjusting Tolerance

The tolerance value depends on your data's precision and acceptable matching range:

| Tolerance | Use Case                                       |
| --------- | ---------------------------------------------- |
| 0.1 K     | High precision data, strict matching           |
| 0.5 K     | Typical lab measurements                       |
| 1.0 K     | Standard industrial data                       |
| 5.0 K     | Rough estimates or very different data sources |

If matching still fails, check:

1. **Data alignment**: `print(sorted(df_exp['temperature_k'].unique()))`
2. **Increase tolerance**: Try 2.0 or 5.0 instead
3. **Column names**: Ensure `left_key` and `right_key` match actual column names

## Merge Type Behavior

- **`how='left'`**: Keep all experimental temperatures, fill with NaN if no prediction found
- **`how='inner'`**: Keep only temperatures that have both experimental and predicted data
- **`how='outer'`**: Keep all temperatures from both datasets
- **`how='right'`**: Keep all predicted temperatures, fill with NaN if no experimental data

For viscosity analysis, **`how='inner'`** is recommended to compare complete pairs.

## Output

The merged dataframe contains all columns from both input dataframes:

```
Columns from experimental data:
  - temperature_k
  - viscosity_mpas
  - log_10_viscosity_mpas

Columns from predicted data:
  - temperature_k (duplicate removed automatically)
  - pred_0
  - log_10_pred_viscosity_mpas

You can then calculate:
  - error = predicted - experimental
  - abs_error = |error|
  - percent_error = (abs_error / experimental) * 100
```

## Notes

- The function preserves the left dataframe's row order
- Duplicate temperatures in either dataframe are handled gracefully
- Missing values (NaN) in the key column are skipped
- For `how='outer'`, unmatched rows will have NaN in columns from the other dataframe
