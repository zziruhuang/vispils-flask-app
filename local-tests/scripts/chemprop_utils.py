"""
Convert human input to chemprop formats

author: ziru huang
ai: claude-haiku-4.5
"""

from pathlib import Path

def create_chemprop_prediction_files(il_smiles: str, 
                                    temperature_k: float = 298.15, 
                                    save_dir = None,
                                    verbose: bool = True) -> dict:
    """Create prediction input files for GNN model (CMPNN/Chemprop).

    Generates the necessary input files in the expected format for the CMPNN/Chemprop model.
    Uses pathlib for robust path handling across platforms.

    Args:
        il_smiles (str): SMILES string representation of the ionic liquid.
        temperature_k (float): Temperature in Kelvin. Default is 298.15 K (25°C).
        save_dir (str or Path, optional): Directory to save files to for chemprop prediction.
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
        ...     save_dir="./model_prediction_files"
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
    if not il_smiles or not isinstance(il_smiles, str):
        error_msg = f"il_smiles must be a non-empty string, got: {il_smiles}"
        if verbose:
            print(f"\n✗ {error_msg}")
        raise ValueError(error_msg)
    
    if temperature_k <= 0:
        error_msg = f"temperature_k must be positive, got: {temperature_k}"
        if verbose:
            print(f"\n✗ {error_msg}")
        raise ValueError(error_msg)
    
    # Convert to Path object and handle default
    if save_dir is None:
        save_dir = Path("./model_prediction_files")
    else:
        save_dir = Path(save_dir)
    
    # Track execution status
    files_created_successfully = False
    error_details = None
    
    try:
        # Create directory if it doesn't exist, gracefully handle existing directories
        try:
            if save_dir.exists():
                if verbose:
                    print(f"ℹ Using existing directory: {save_dir.resolve()}")
            else:
                save_dir.mkdir(parents=True, exist_ok=True)
                if verbose:
                    print(f"✓ Created new directory: {save_dir.resolve()}")
        except OSError as e:
            error_details = f"Failed to create/access directory {save_dir}: {e}"
            raise OSError(error_details)
        
        # Define file paths
        smis_path = save_dir / "data-smis.csv"
        descs_path = save_dir / "data-descs.csv"
        predict_out_path = save_dir / "Predict.csv"
        
        # Write SMILES file
        with open(smis_path, "w") as smis_f:
            smis_f.write("il_smiles,log_10_viscosity_mpas\n")
            smis_f.write(f"{il_smiles},0\n")
        if verbose:
            print(f"✓ Created SMILES file: {smis_path}")
        
        # Write descriptors file
        with open(descs_path, "w") as descs_f:
            descs_f.write("temperature_k\n")
            descs_f.write(f"{temperature_k}\n")
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
        'smiles': smis_path,
        'descriptors': descs_path,
        'output': predict_out_path,
        'directory': save_dir
    }
    
    # Print success summary
    if verbose and files_created_successfully:
        print("\n=== Model Prediction Files Ready ===")
        for key, path in results.items():
            print(f"{key}: {path}")

    
    return results
