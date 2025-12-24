"""
Convert human input to chemprop formats

author: ziru huang
ai: claude-haiku-4.5
"""

from pathlib import Path
import os


def to_display_path(p):
    """Convert a Path to a relative path string for display using os.path.relpath."""
    try:
        return os.path.relpath(str(p), os.getcwd())
    except (ValueError, TypeError):
        return str(p)

def create_chemprop_input_files(il_smiles: list[str], 
                                temperature_k: list[int|float] = [298.15], 
                                input_files_dir=None,
                                verbose: bool = True) -> dict:
    """Create prediction input files for GNN model (CMPNN/Chemprop).

    Generates the necessary input files in the expected format for the CMPNN/Chemprop model.
    Uses pathlib for robust path handling across platforms.

    Args:
        il_smiles (str): SMILES string representation of the ionic liquid.
        temperature_k (float): Temperature in Kelvin. Default is 298.15 K (25°C).
        input_files_dir (str or Path, optional): Directory to save files to for chemprop prediction.
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
        >>> paths = create_chemprop_input_files(
        ...     il_smiles="CCCCn1cc[n+](C)c1.F[B-](F)(F)F",
        ...     temperature_k=298.15,
        ...     input_files_dir="./model_prediction_files"
        ... )
        >>> 
        >>> # Silent mode for scripting
        >>> paths = create_chemprop_input_files(
        ...     il_smiles="CCCCn1cc[n+](C)c1.F[B-](F)(F)F",
        ...     temperature_k=298.15,
        ...     verbose=False
        ... )
    """
    
    # Input validation
    if not il_smiles or not isinstance(il_smiles, list) or not all(isinstance(s, str) and s for s in il_smiles):
        raise ValueError(f"il_smiles must be a non-empty list of strings, got: {il_smiles}")

    if not temperature_k or not all(isinstance(t, (int, float)) and t > 0 for t in temperature_k):
        raise ValueError(f"temperature_k must be a list of positive numbers, got: {temperature_k}")

    # Convert to Path object and handle default
    if input_files_dir is None:
        input_files_dir = Path("./model_input_files")
    else:
        input_files_dir = Path(input_files_dir)
    
    # Create directory if it doesn't exist, gracefully handle existing directories
    try:
        if input_files_dir.exists():
            if verbose:
                print(f"ℹ Using existing directory: {to_display_path(input_files_dir)}")
        else:
            input_files_dir.mkdir(parents=True, exist_ok=True)
            if verbose:
                print(f"✓ Created new directory: {to_display_path(input_files_dir)}")
    except OSError as e:
        raise OSError(f"Failed to create/access directory {input_files_dir}: {e}")
    
    # Define file paths
    smiles_path = input_files_dir / "input_smiles.csv"
    descs_path = input_files_dir / "input_descs.csv"
    
    try:
        # Write SMILES file
        with open(smiles_path, "w") as smiles_f:
            smiles_f.write("il_smiles,log_10_viscosity_mpas\n")
            for il in il_smiles:
                smiles_f.write(f"{il},0\n")
        if verbose:
            print(f"✓ Created SMILES file: {str(smiles_path.resolve())}")
        
        # Write descriptors file
        with open(descs_path, "w") as descs_f:
            descs_f.write("temperature_k\n")
            for t in temperature_k:
                descs_f.write(f"{t}\n")
        if verbose:
            print(f"✓ Created descriptors file: {str(descs_path.resolve())}")
        
    except OSError as e:
        raise OSError(f"Failed to write prediction files: {e}")
    
    # Create results dictionary
    results = {
        'smiles': smiles_path,
        'descriptors': descs_path,
        'directory': input_files_dir
    }
    
    # Print summary (only if verbose)
    if verbose:
        print("\n=== Model Input Files Ready ===")
        for key, path in results.items():
            print(f"{key}: {to_display_path(path)}")
    
    return results


import subprocess

def run_chemprop_prediction(input_files_dir="./model_input_files",
                            predict_script_path="./predict.py",
                            model_checkpoint_path="./models/model.pt",
                            dry_run=True,
                            verbose=True) -> dict:
    """Run Chemprop prediction with robust error handling.
    
    Executes the Chemprop prediction script with validated input files and model checkpoint.
    Handles path resolution, file validation, and model checkpoint discovery.
    
    Args:
        input_files_dir (str or Path): Directory containing prediction input files
                                          (data-smiles.csv, data-descs.csv).
        predict_script_path (str or Path): Path to the Chemprop prediction script.
        model_checkpoint_path (str or Path): Path to model checkpoint (.pt file) or
                                            directory containing .pt files.
        dry_run (bool): If True, prints command without executing. Default is True.
        verbose (bool): If True, prints progress messages and results. Default is True.
    
    Returns:
        dict: Dictionary containing:
              - 'success': bool indicating if prediction completed successfully
              - 'command': str of the executed command
              - 'stdout': str output from the prediction script
              - 'stderr': str error output from the prediction script
              - 'output_path': Path to the prediction output file
              - 'return_code': int return code from subprocess
    
    Raises:
        FileNotFoundError: If any required file/directory is not found.
        ValueError: If required input files are missing.
        OSError: If subprocess execution fails.
    
    Example:
        >>> result = run_chemprop_prediction(
        ...     input_files_dir="./model_prediction_files",
        ...     predict_script_path="../../vispils/predict.py",
        ...     model_checkpoint_path="../../vispils/models/model.pt",
        ...     dry_run=False
        ... )
        >>> if result['success']:
        ...     print(f"Predictions saved to {result['output_path']}")
    """
    # Store original input paths for display purposes
    input_files_dir_display = input_files_dir
    predict_script_path_display = predict_script_path
    model_checkpoint_path_display = model_checkpoint_path
    
    # Convert all paths to Path objects and resolve them
    input_files_dir = Path(input_files_dir).resolve()
    predict_script_path = Path(predict_script_path).resolve()
    model_checkpoint_path = Path(model_checkpoint_path).resolve()
    
    # Validate all required paths exist
    if not input_files_dir.exists():
        raise FileNotFoundError(f"Chemprop files directory not found: {input_files_dir}")
    if not predict_script_path.exists():
        raise FileNotFoundError(f"Prediction script not found: {predict_script_path}")
    if not model_checkpoint_path.exists():
        raise FileNotFoundError(f"Model checkpoint path not found: {model_checkpoint_path}")
    
    if verbose:
        print("✓ Validated input paths:")
        print(f"  - Input files: {str(Path(input_files_dir))}")
        print(f"  - Script: {str(Path(predict_script_path))}")
        print(f"  - Checkpoint: {str(Path(model_checkpoint_path))}")
    
    # Define expected input files
    smiles_path = input_files_dir / "input_smiles.csv"
    descs_path = input_files_dir / "input_descs.csv"
    predict_out_path = input_files_dir / "predict.csv"
    
    # Validate input files exist
    if not smiles_path.exists():
        raise ValueError(f"SMILES input file not found: {smiles_path}")
    if not descs_path.exists():
        raise ValueError(f"Descriptors input file not found: {descs_path}")
    
    if verbose:
        print(f"✓ Found input files: {smiles_path.name}, {descs_path.name}")
    
    # Find model checkpoint .pt file
    actual_checkpoint_path = None
    if model_checkpoint_path.suffix == ".pt":
        actual_checkpoint_path = model_checkpoint_path
    else:
        # Search for .pt files in the directory
        pt_files = list(model_checkpoint_path.rglob("*.pt"))
        if not pt_files:
            raise FileNotFoundError(f"No .pt checkpoint files found in: {model_checkpoint_path}")
        
        if verbose:
            for pt in pt_files:
                print(f"  Found checkpoint: {pt.relative_to(model_checkpoint_path)}")
        
        # Use the first found .pt file (or could use most recent)
        actual_checkpoint_path = pt_files[0].parent
    
    if verbose:
        print(f"✓ Using model checkpoint in: {str(actual_checkpoint_path)}")
    
    # Build the command (use absolute paths for actual execution)
    cmd = [
        "python", str(predict_script_path),
        "--data_path", str(smiles_path),
        "--features_path", str(descs_path),
        "--save_dir", str(predict_out_path.parent),
        "--checkpoint_path", str(actual_checkpoint_path),
        "--hidden_size", "100",
        "--no_cuda"
    ]
    
    # Build display command (use relative paths for readability)
    cmd_display = [
        "python", to_display_path(predict_script_path),
        "--data_path", to_display_path(smiles_path),
        "--features_path", to_display_path(descs_path),
        "--save_dir", to_display_path(predict_out_path.parent),
        "--checkpoint_path", to_display_path(actual_checkpoint_path),
        "--hidden_size", "100",
        "--no_cuda"
    ]
    
    # Prepare result dictionary
    result = {
        'success': False,
        'command': " \\\n  ".join(cmd_display),
        'stdout': "",
        'stderr': "",
        'output_path': predict_out_path,
        'return_code': None
    }
    
    if dry_run:
        if verbose:
            print("\n=== Dry Run Mode ===")
            print("Command to be executed:")
            print(result['command'])
        return result
    
    # Execute the prediction script
    try:
        if verbose:
            print("\n=== Executing Prediction Script ===")
            print(f"Command: {result['command']}\n")
        
        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            timeout=300  # 5 minute timeout
        )
        
        result['stdout'] = process.stdout
        result['stderr'] = process.stderr
        result['return_code'] = process.returncode
        result['success'] = process.returncode == 0
        
        if verbose:
            if result['success']:
                print("✓ Prediction completed successfully!")
                if process.stdout:
                    print(f"\nScript output:\n{process.stdout}")
                print(f"\n✓ Predictions saved to: {predict_out_path}")
            else:
                print("✗ Prediction script failed!")
                print(f"Return code: {process.returncode}")
                if process.stderr:
                    print(f"Error output:\n{process.stderr}")
                if process.stdout:
                    print(f"Standard output:\n{process.stdout}")
        
    except subprocess.TimeoutExpired:
        error_msg = "Prediction script execution timed out (5 minute limit)"
        result['stderr'] = error_msg
        if verbose:
            print(f"✗ {error_msg}")
    except Exception as e:
        error_msg = f"Failed to execute prediction script: {e}"
        result['stderr'] = error_msg
        if verbose:
            print(f"✗ {error_msg}")
    
    return result


import pandas as pd
import numpy as np

def process_chemprop_results(predict_output_path: Path,
                             viscosity_format: str = "mpas",
                             verbose: bool = True) -> list[float]:
    """Process Chemprop prediction results to extract viscosity predictions.
    
    Reads the prediction output CSV file and extracts the predicted viscosity values.
    
    Args:
        predict_output_path (str or Path): Path to the Chemprop prediction output CSV file.
        verbose (bool): If True, prints progress messages. Default is True.
    
    Returns:
        list[float]: List of predicted viscosity values in mPa·s.
    
    Raises:
        FileNotFoundError: If the prediction output file is not found.
        ValueError: If the output file format is invalid or missing expected columns.
    
    Example:
        >>> viscosities = process_chemprop_results(
        ...     predict_output_path="./model_input_files/predict.csv"
        ... )
        >>> print(viscosities)
    """
    predict_output_path = Path(predict_output_path).resolve()
    
    if not predict_output_path.exists():
        raise FileNotFoundError(f"Prediction output file not found: {predict_output_path}")
    
    if predict_output_path.suffix.lower() != ".csv":
        raise ValueError(f"Prediction output file must be a .csv file, got: {predict_output_path.suffix}")
    
    df_prediction = pd.read_csv(predict_output_path)
    
    pred_cols = [col for col in df_prediction.columns if col.startswith("pred_")]

    if viscosity_format == "mpas":
        pass  # Already in mPa·s
    elif viscosity_format == "pas":
        df_prediction[pred_cols] = df_prediction[pred_cols] / 1000  # Convert to Pa·s
    elif viscosity_format == "log mpas":
        df_prediction[pred_cols] = np.exp(df_prediction[pred_cols])
    elif viscosity_format == "log 10 mpas":
        df_prediction[pred_cols] = 10**(df_prediction[pred_cols])
    else:
        raise ValueError(f"Unsupported viscosity_format: {viscosity_format}. Please use 'mpas', 'pas', 'log mpas', or 'log 10 mpas'.")

    return df_prediction