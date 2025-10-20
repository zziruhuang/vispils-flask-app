import pandas as pd
from IPython.display import display
import os

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


# Default column mapping for standardizing old dataset column names
DEFAULT_RENAME_COLS = {
    "Dataset": "reference",
    "Iso SMILES": "sanitized_il_smiles",
    "cSMILES": "cation_smiles",
    "aSMILES": "anion_smiles",
    "Pressure": "pressure_atm",
    "Temperature": "temperature_k", 
    "Viscosity": "viscosity_mpas",
    "Log viscosity": "log_10_viscosity_mpas",
    "cfam": "cation_family",
    "afam": "anion_family",
    "cvolume": "cation_volume_rdkit",
    "avolume": "anion_volume_rdkit",
}

def rename_cols_df(df: pd.DataFrame, inplace=False, rename_cols=None) -> pd.DataFrame:
    """Rename columns to standardized names for old dataset format.
     
    This function renames the old dataset column names to more standardized,
    snake_case naming conventions. It handles missing columns gracefully.
     
    Args:
        df (pd.DataFrame): The dataframe to rename columns in.
        inplace (bool): If True, modifies the dataframe in-place and returns df.
                       If False, returns a new dataframe with renamed columns.
                       Default is False.
        rename_cols (dict, optional): Custom mapping of old column names to new names.
                                      If None, uses DEFAULT_RENAME_COLS.
                                      Default is None.
     
    Returns:
        pd.DataFrame: The dataframe with renamed columns (same object if inplace=True,
                      new copy if inplace=False).
     
    Example:
        >>> df = pd.read_csv('data.csv')
        >>> df_renamed = rename_cols_df(df, inplace=False)
        >>> # Or with custom mapping:
        >>> custom_mapping = {'OldName': 'new_name', 'Another': 'renamed'}
        >>> # Or with merged mapping:
        >>> merged_mapping = {**DEFAULT_RENAME_COLS, 'CustomCol': 'custom_new_name'}
        >>> df_renamed = rename_cols_df(df, rename_cols=merged_mapping)
        >>> df.rename_cols_df(df, rename_cols=custom_mapping)

    """
    
    # Use default if no custom mapping provided
    if rename_cols is None:
        rename_cols = DEFAULT_RENAME_COLS.copy()
    
    # Check which columns exist in the dataframe
    existing_renames = {old: new for old, new in rename_cols.items() 
                       if old in df.columns}
    
    if not existing_renames:
        print(f"Warning: No columns found to rename. Available columns: {list(df.columns)}")
        return df.copy() if not inplace else df
    else:
        print(f"Renaming {len(existing_renames)} columns: {list(existing_renames.keys())}")
    
    # Log missing columns
    missing_cols = set(rename_cols.keys()) - set(df.columns)
    if missing_cols:
        print(f"Info: The following columns were not found and not renamed: {missing_cols}")
    
    # Apply renaming
    df_renamed = df.rename(columns=existing_renames, inplace=inplace)

    return df_renamed if not inplace else df


class dfUtils(pd.core.frame.DataFrame):
    """Extend pandas DataFrame with custom methods
    author: ziru huang

    Args:
        pd (DataFrame): pandas DataFrame object
    """
    def data_summary(self, il_smiles_col="Iso SMILES", temp_col="Temperature"):
        """Display summary statistics of the dataframe."""
        
        print("\n====== data summary ======\n")
        print(f"Total data points ({len(self)})")
        print(f"Unique IL SMILES ({len(self[il_smiles_col].unique())})")
        
        columns = self.columns

        for k, v in [("Unique temperatures", self[temp_col].unique()), ("Columns", columns)]:
            if len(v) > 25:
                v = sorted(v)[:25]
            print(f"{k} ({len(v)}): {v}")

        display(self.head())


    def sanitize_old_df(self, inplace=True, rename_cols=None):
        """Rename columns to standardized names for old dataset format.
        
        This method provides a convenient wrapper around rename_cols_df() for use
        with dfUtils instances. It allows flexible column renaming with custom mappings.
        
        Args:
            inplace (bool): If True, modifies the dataframe in-place and returns self.
                          If False, returns a new dataframe with renamed columns.
                          Default is True for method chaining compatibility.
            rename_cols (dict, optional): Custom mapping of old column names to new names.
                                         If None, uses DEFAULT_RENAME_COLS.
                                         Default is None.
        
        Returns:
            pd.DataFrame or dfUtils: Self if inplace=True, otherwise a new DataFrame 
                                     (or dfUtils object) with renamed columns.
        
        Example:
            >>> df = dfUtils(pd.read_csv('data.csv'))
            >>> df.sanitize_old_df()  # Uses default mapping, modifies in-place
            >>> 
            >>> # With custom column mapping:
            >>> custom_mapping = {'TempC': 'temperature_k', 'ViscMPa': 'viscosity_mpas'}
            >>> df_renamed = df.sanitize_old_df(inplace=False, rename_cols=custom_mapping)
        """
        return rename_cols_df(self, inplace=inplace, rename_cols=rename_cols)
