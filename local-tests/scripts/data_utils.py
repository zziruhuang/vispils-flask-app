import pandas as pd
from IPython.display import display
import os

#===============================
#    CSV Data Quick Loading
#===============================

def load_csv_info(filepath):
    """Get file size, row count, column count, and column names without loading entire file into memory."""
    file_size_mb = os.path.getsize(filepath) / (1024 * 1024)
    
    # Read just the header to get column info
    df_header = pd.read_csv(filepath, nrows=0)
    column_count = len(df_header.columns)
    column_names = df_header.columns.tolist()
    
    # Count rows
    row_count = sum(1 for _ in open(filepath)) - 1  # Subtract header
    
    print(f"File: {os.path.basename(filepath)}")
    print(f"Size: {file_size_mb:.2f} MB")
    print(f"Rows: {row_count:,}")
    print(f"Columns: {column_count}")
    print(f"Column Names: {column_names}")
    
    return file_size_mb, row_count, column_count, column_names

def load_csv_chunked(filepath, chunksize=5000, columns=None):
    """Load CSV in chunks. Yields dataframes of specified chunksize."""
    print(f"Loading {os.path.basename(filepath)} in chunks of {chunksize}...")
    for chunk in pd.read_csv(filepath, chunksize=chunksize, usecols=columns):
        yield chunk

def load_csv_sample(filepath, nrows=1000):
    """Load only first n rows for quick inspection."""
    return pd.read_csv(filepath, nrows=nrows)

def load_csv_filtered(filepath, filter_dict=None, columns=None):
    """Load CSV with filtering to reduce memory usage.
    
    Args:
        filepath: Path to CSV file
        filter_dict: Dict of column filters, e.g., {'Temperature': (300, 400)}
        columns: List of columns to load
    """
    df = pd.read_csv(filepath, usecols=columns)
    if filter_dict:
        for col, (min_val, max_val) in filter_dict.items():
            df = df[(df[col] >= min_val) & (df[col] <= max_val)]
    return df


# ===============================
#   DataFrame Column Renaming
# ===============================

DEFAULT_RENAME_COLS = {
    #"DataSource": "data_origin",
    #"Dataset": "reference_doi",
    "Dataset": "reference",
    # property column names
    "Iso SMILES": "il_smiles",
    "cSMILES": "cation_smiles",
    "aSMILES": "anion_smiles",
    "Pressure": "pressure_atm",
    "Temperature": "temperature_k", 
    "Viscosity": "viscosity_mpas",
    'η (mPas)': "viscosity_mpas",
    "Log viscosity": "log_10_viscosity_mpas",
    # chemical structure derived category column names
    "cfam": "cation_family_v0",
    "afam": "anion_family_v0",
    'cfam1': "cation_family",
    'afam1': "anion_family",
    'cfam_class': "cation_class",
    'afam_class': "anion_class",
    'cFGs': "cation_functional_group",
    'aFGs': "anion_functional_group",
    'cFGsGroup': "cation_functional_group_class",
    'aFGsGroup': "anion_functional_group_class",
    # descriptor columns names
    # "cvolume": "cation_volume_rdkit",
    # "avolume": "anion_volume_rdkit",
}

def rename_df_cols(df: pd.DataFrame, inplace=False, rename_cols=None) -> pd.DataFrame:
    """Rename specified columns only - keep all other columns unchanged.
     
    This function selectively renames only the columns specified in the mapping dictionary.
    All other columns remain untouched. It handles missing columns gracefully by only
    renaming those that exist in the dataframe.
     
    Args:
        df (pd.DataFrame): The dataframe to rename columns in.
        inplace (bool): If True, modifies the dataframe in-place and returns df.
                       If False, returns a new dataframe with renamed columns.
                       Default is False.
        rename_cols (dict, optional): Custom mapping of old column names to new names.
                                      Only columns in this dictionary will be renamed.
                                      If None, uses DEFAULT_RENAME_COLS.
                                      Default is None.
     
    Returns:
        pd.DataFrame: The dataframe with specified columns renamed. All other columns 
                      remain unchanged (same object if inplace=True, new copy if inplace=False).
     
    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({
        ...     'Temperature': [273.15, 283.15],
        ...     'η (mPas)': [10.5, 12.3],
        ...     'OtherColumn': [1, 2]  # This stays unchanged
        ... })
        >>> # With custom mapping - only renames specified columns
        >>> custom_mapping = {'Temperature': 'temperature_k', 'η (mPas)': 'viscosity_mpas'}
        >>> df_renamed = rename_df_cols(df, rename_cols=custom_mapping, inplace=False)
        >>> print(df_renamed.columns)
        # Output: Index(['temperature_k', 'viscosity_mpas', 'OtherColumn'], dtype='object')

    """
    
    # Use default if no custom mapping provided
    if rename_cols is None:
        rename_cols = DEFAULT_RENAME_COLS.copy()
    
    # Filter to only columns that exist in the dataframe
    # This ensures we only rename what we specify, leaving all others unchanged
    existing_renames = {old: new for old, new in rename_cols.items() if old in df.columns}
    
    if not existing_renames:
        print(f"⚠️  Warning: No columns found to rename.")
        print(f"   Available columns: {list(df.columns)}")
        print(f"   Requested to rename: {list(rename_cols.keys())}")
        return df.copy() if not inplace else df
    
    # Report what we're renaming
    print(f"✓ Renaming {len(existing_renames)} column(s):")
    for old, new in existing_renames.items():
        print(f"  '{old}' → '{new}'")
    
    # Log columns that were not found (not an error, just info)
    missing_cols = set(rename_cols.keys()) - set(df.columns)
    if missing_cols:
        print(f"ℹ️  Note: {len(missing_cols)} column(s) not found (not renamed):")
        for col in missing_cols:
            print(f"  - '{col}'")
    
    # Log columns that remain unchanged
    unchanged = set(df.columns) - set(existing_renames.keys())
    print(f"ℹ️  {len(unchanged)} column(s) remain unchanged")
    
    # Apply renaming - only specified columns are renamed, all others stay the same
    df_renamed = df.rename(columns=existing_renames, inplace=inplace)

    return df_renamed if not inplace else df

def group_summary(df, group_col):
    """Display summary statistics for a specified grouping column in the dataframe."""
    
    # Validate column
    if group_col not in df.columns:
        raise ValueError(f"Column '{group_col}' not found in dataframe.")
    
    print(f"\nGroup summary by {group_col}:")
    print(f"number of unique {group_col}: {df[group_col].nunique()}")
    print('-'*40)
    display(df.groupby(group_col).size())
    print('-'*40)

# =======================================
#   Merge on Temperature with Tolerance
# =======================================

def merge_with_tolerance(df_left: pd.DataFrame, 
                        df_right: pd.DataFrame,
                        left_key: str = 'temperature_k',
                        right_key: str = 'temperature_k',
                        tolerance: float = 1.0,
                        how: str = 'left') -> pd.DataFrame:
    """Merge two dataframes based on a numeric column with tolerance.
    
    This function performs a "fuzzy" merge where numeric keys must be within
    a specified tolerance range rather than matching exactly. Useful for merging
    experimental and predicted data that may have slightly different temperature
    values due to rounding or precision differences.
    
    Args:
        df_left (pd.DataFrame): Left dataframe to merge from.
        df_right (pd.DataFrame): Right dataframe to merge from.
        left_key (str): Column name in df_left to match on. Default is 'temperature_k'.
        right_key (str): Column name in df_right to match on. Default is 'temperature_k'.
        tolerance (float): Tolerance range for matching. A left value matches a right
                          value if abs(left - right) <= tolerance. Default is 1.0.
        how (str): Type of merge - 'left', 'right', 'inner', or 'outer'.
                   Default is 'left'.
    
    Returns:
        pd.DataFrame: Merged dataframe with matched rows based on tolerance.
    
    Example:
        >>> # Merge experimental data (273.15 K) with predicted data (273 K)
        >>> df_exp = pd.DataFrame({'temperature_k': [273.15, 283.15, 298.15], 
        ...                         'viscosity': [10.5, 5.2, 2.1]})
        >>> df_pred = pd.DataFrame({'temperature_k': [273, 283, 298],
        ...                          'predicted_viscosity': [10.3, 5.1, 2.2]})
        >>> df_merged = merge_with_tolerance(df_exp, df_pred, tolerance=1.0)
        >>> # All rows match because differences are <= 1.0 K
    """
    import numpy as np
    
    # Create a merge key for matching within tolerance
    def find_matches(left_val, right_series, tol):
        """Find all indices in right_series within tolerance of left_val"""
        distances = np.abs(right_series - left_val)
        return distances <= tol
    
    # Initialize result list
    matched_rows = []
    
    # For each row in left dataframe
    for left_idx, left_row in df_left.iterrows():
        left_val = left_row[left_key]
        
        # Find matching rows in right dataframe
        matches = find_matches(left_val, df_right[right_key], tolerance)
        matching_indices = df_right[matches].index.tolist()
        
        if matching_indices:
            # For each match, merge the rows
            for right_idx in matching_indices:
                right_row = df_right.loc[right_idx]
                
                # Start with left row to preserve its columns
                merged_dict = left_row.to_dict()
                
                # Add columns from right row (skip if key column with same name)
                for col in right_row.index:
                    if col != right_key or left_key != right_key:
                        # Don't overwrite left key column with right key column if they're the same
                        merged_dict[col] = right_row[col]
                
                merged_row = pd.Series(merged_dict)
                matched_rows.append(merged_row)
        else:
            # No match found - behavior depends on 'how' parameter
            if how in ['left', 'outer']:
                merged_dict = left_row.to_dict()
                # Add NaN columns from right df
                for col in df_right.columns:
                    if col not in merged_dict:
                        merged_dict[col] = np.nan
                merged_row = pd.Series(merged_dict)
                matched_rows.append(merged_row)
    
    # Handle 'right' and 'outer' joins for unmatched right rows
    if how in ['right', 'outer']:
        matched_left_indices = set()
        for left_idx, left_row in df_left.iterrows():
            left_val = left_row[left_key]
            matches = find_matches(left_val, df_right[right_key], tolerance)
            if matches.any():
                matched_left_indices.add(left_idx)
        
        for right_idx, right_row in df_right.iterrows():
            right_val = right_row[right_key]
            matches = find_matches(right_val, df_left[left_key], tolerance)
            
            if not matches.any():
                # This right row has no match
                merged_dict = right_row.to_dict()
                # Add NaN columns from left df
                for col in df_left.columns:
                    if col not in merged_dict:
                        merged_dict[col] = np.nan
                merged_row = pd.Series(merged_dict)
                matched_rows.append(merged_row)
    
    if not matched_rows:
        return pd.DataFrame()
    
    result = pd.DataFrame(matched_rows)
    return result.reset_index(drop=True)

# =======================================
#   Extended DataFrame Class
# =======================================

class dfUtils(pd.core.frame.DataFrame):
    """Extend pandas DataFrame with custom methods
    author: ziru huang

    Args:
        pd (DataFrame): pandas DataFrame object

    Returns:
        dfUtils: Extended DataFrame with additional methods

    """
    def data_summary(self, head = 5,
                     smiles_col="il_smiles", temperature_col="temperature_k"):
        """Display summary statistics of the dataframe."""
        
        # Validate columns
        if smiles_col not in self.columns:
            raise ValueError(f"Column '{smiles_col}' not found in dataframe. Might be 'Iso SMILES' or 'il_smiles'.")
        if temperature_col not in self.columns:
            raise ValueError(f"Column '{temperature_col}' not found in dataframe. Might be 'Temperature' or 'temperature_k'.")

        print("\n====== data summary ======\n")
        print(f"Total data points ({len(self)})")
        print(f"Unique IL SMILES ({len(self[smiles_col].unique())})")
        
        columns = self.columns

        for k, v in [("Unique temperatures", self[temperature_col].unique()), ("Columns", columns)]:
            if len(v) > 25:
                v = sorted(v)[:25]
            print(f"{k} ({len(columns)}): {v}")

        if head is not None and head > 0:
            print("\nDataframe head:")
            display(self.head(head))


    def sanitize_old_df_cols(self, inplace=True, rename_cols=None):
        """Rename specified columns only - keep all other columns unchanged.
        
        This method selectively renames only the columns provided in the dictionary.
        All other columns remain untouched. Perfect for standardizing column names
        while preserving additional columns.
        
        Args:
            inplace (bool): If True, modifies the dataframe in-place and returns self.
                          If False, returns a new dataframe with renamed columns.
                          Default is True for method chaining compatibility.
            rename_cols (dict, optional): Mapping of old column names to new names.
                                         Only columns in this dictionary will be renamed.
                                         All other columns stay unchanged.
                                         If None, uses DEFAULT_RENAME_COLS.
                                         Default is None.
        
        Returns:
            pd.DataFrame or dfUtils: Self if inplace=True, otherwise a new DataFrame 
                                     (or dfUtils object) with specified columns renamed
                                     and all other columns preserved.
        
        Example:
            >>> df = dfUtils(pd.read_csv('data.csv'))
            >>> # Rename only specified columns, keep the rest unchanged
            >>> custom_mapping = {
            ...     'Temperature': 'temperature_k',
            ...     'η (mPas)': 'viscosity_mpas'
            ... }
            >>> df_renamed = df.sanitize_old_df_cols(inplace=False, rename_cols=custom_mapping)
            >>> # Any other columns in the dataframe remain with original names
        """

        return rename_df_cols(self, inplace=inplace, rename_cols=rename_cols)
