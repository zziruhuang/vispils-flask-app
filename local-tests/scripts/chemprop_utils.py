"""
Convert human input to chemprop formats

author: ziru huang
ai: claude-haiku-4.5
"""

from pathlib import Path

def create_chemprop_prediction_files(il_smiles: list, 
                                     temperature_k: list = [298.15], 
                                     chemprop_files_dir = None,
                                     verbose: bool = True) -> dict:
    """Create prediction input files for GNN model (CMPNN/Chemprop).

    Generates the necessary input files in the expected format for the CMPNN/Chemprop model.
    Uses pathlib for robust path handling across platforms.

    Args:
        il_smiles (str): SMILES string representation of the ionic liquid.
        temperature_k (float): Temperature in Kelvin. Default is 298.15 K (25°C).
        chemprop_files_dir (str or Path, optional): Directory to save files to for chemprop prediction.
                                          If None, uses './model_prediction_files'.
                                          Will be created if it doesn't exist.
        verbose (bool): If True, prints progress messages and summary. If False, runs silently.
                       Default is True.

    Returns:
        dict: Dictionary containing paths to created files:
              - 'smiles': Path to SMILES input file
              - 'descriptors': Path to descriptors input file
              - 'output': Path where predictions will be saved
              - 'directory': Path to the directory containing the files
    
    Raises:
        ValueError: If il_smiles is empty or temperature_k is not positive.
        OSError: If files cannot be created due to permission or filesystem issues.
    
    Example:
        >>> # With verbose output (default)
        >>> paths = create_chemprop_prediction_files(
        ...     il_smiles="CCCCn1cc[n+](C)c1.F[B-](F)(F)F",
        ...     temperature_k=298.15,
        ...     chemprop_files_dir="./model_prediction_files"
        ... )
        >>> 
        >>> # Silent mode for scripting
        >>> paths = create_chemprop_prediction_files(
        ...     il_smiles="CCCCn1cc[n+](C)c1.F[B-](F)(F)F",
        ...     temperature_k=298.15,
        ...     verbose=False
        ... )
    """
    
    # Input validation
    if not il_smiles or not isinstance(il_smiles, list):
        error_msg = f"il_smiles must be a non-empty list (str), got: {il_smiles}"
        if verbose:
            print(f"\n✗ {error_msg}")
        raise ValueError(error_msg)
    
    if not temperature_k or not all(isinstance(temp, (int, float)) for temp in temperature_k):
        error_msg = f"temperature_k must be a non-empty list of numbers (int, float), got: {temperature_k}"
        if verbose:
            print(f"\n✗ {error_msg}")
        raise ValueError(error_msg)
    
    # Convert to Path object and handle default
    if chemprop_files_dir is None:
        chemprop_files_dir = Path("./model_prediction_files")
    else:
        chemprop_files_dir = Path(chemprop_files_dir)
    
    # Track execution status
    files_created_successfully = False
    error_details = None
    
    try:
        # Create directory if it doesn't exist, gracefully handle existing directories
        try:
            if chemprop_files_dir.exists():
                if verbose:
                    print(f"ℹ Using existing directory: {chemprop_files_dir.resolve()}")
            else:
                chemprop_files_dir.mkdir(parents=True, exist_ok=True)
                if verbose:
                    print(f"✓ Created new directory: {chemprop_files_dir.resolve()}")
        except OSError as e:
            error_details = f"Failed to create/access directory {chemprop_files_dir}: {e}"
            raise OSError(error_details)
        
        # Define file paths
        smiles_path = chemprop_files_dir / "data-smiles.csv"
        descs_path = chemprop_files_dir / "data-descs.csv"
        predict_out_path = chemprop_files_dir / "Predict.csv"
        
        # Write SMILES file
        with open(smiles_path, "w") as smiles_f:
            smiles_f.write("il_smiles,log_10_viscosity_mpas\n")
            for il in il_smiles:
                smiles_f.write(f"{il},0\n")
        if verbose:
            print(f"✓ Created SMILES file: {smiles_path}")

        # Write descriptors file
        with open(descs_path, "w") as descs_f:
            descs_f.write("temperature_k\n")
            for t in temperature_k:
                descs_f.write(f"{t}\n")
        if verbose:
            print(f"✓ Created descriptors file: {descs_path}")
            print(f"✓ Predictions will be saved to: {predict_out_path}")
        
        # If we reach here, all files were created successfully
        files_created_successfully = True
        
    except (OSError, IOError) as e:
        error_details = str(e)
        raise OSError(f"Failed to write prediction files: {e}")
    
    # Create results dictionary
    results = {
        'smiles': smiles_path,
        'descriptors': descs_path,
        'output': predict_out_path,
        'directory': chemprop_files_dir
    }
    
    # Print success summary
    if verbose and files_created_successfully:
        print("\n=== Model Prediction Files Ready ===")
        for key, path in results.items():
            print(f"{key}: {path}")

    
    return results
