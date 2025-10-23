"""
Ionic Liquid Viscosity Prediction Pipeline
==========================================

A professional, reusable pipeline for querying IL viscosity data and generating
predictions using Graph Convolutional Neural Networks (GCNN).

Author: Ziru Huang
Date: October 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import os
import sys

# Local imports (adjust as needed)
from data_utils import dfUtils, merge_with_tolerance, rename_cols_df
from smiles_utils import sanitized_smiles
from chemprop_utils import create_chemprop_input_files, run_chemprop_prediction, process_chemprop_results


class ILViscosityPipeline:
    """
    End-to-end pipeline for IL viscosity prediction.
    
    Workflow:
        1. Load and sanitize experimental data
        2. Query specific IL from database
        3. Create input files for GCNN model
        4. Run predictions
        5. Analyze and compare with experimental data
        6. Generate visualizations and reports
    
    Attributes:
        data_path (Path): Path to VISPILS dataset CSV
        model_checkpoint_path (Path): Path to trained model directory
        predict_script_path (Path): Path to prediction script
        temperature_tolerance (float): Tolerance for temperature matching (K)
        output_dir (Path): Directory for outputs
    """
    
    def __init__(self,
                 data_path: str = "../../vispils/data/data_vispils.csv",
                 model_checkpoint_path: str = "../../vispils/models/model-corr-5-temp-100-3-2-scale3-constrain-seed42",
                 predict_script_path: str = "../../vispils/predict.py",
                 temperature_tolerance: float = 1.0,
                 output_dir: str = "./pipeline_output",
                 verbose: bool = True):
        """
        Initialize the pipeline with paths and configuration.
        
        Args:
            data_path: Path to experimental data CSV
            model_checkpoint_path: Path to trained model checkpoint
            predict_script_path: Path to prediction script
            temperature_tolerance: Temperature matching tolerance in K
            output_dir: Directory to save outputs
            verbose: Print progress messages
        """
        self.data_path = Path(data_path)
        self.model_checkpoint_path = Path(model_checkpoint_path)
        self.predict_script_path = Path(predict_script_path)
        self.temperature_tolerance = temperature_tolerance
        self.output_dir = Path(output_dir)
        self.verbose = verbose
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize data storage
        self.df_full = None
        self.df_query = None
        self.df_results = None
        self.df_comparison = None
        
        # IL information
        self.il_smiles_original = None
        self.il_smiles_sanitized = None
        self.cation_smiles = None
        self.anion_smiles = None
        
        if self.verbose:
            print("=" * 70)
            print("IL Viscosity Prediction Pipeline Initialized")
            print("=" * 70)
            print(f"Data path: {self.data_path}")
            print(f"Model: {self.model_checkpoint_path}")
            print(f"Temperature tolerance: {self.temperature_tolerance} K")
            print(f"Output directory: {self.output_dir}")
            print()
    
    def load_experimental_data(self) -> pd.DataFrame:
        """
        Load and sanitize experimental viscosity data.
        
        Returns:
            pd.DataFrame: Sanitized dataframe with standardized columns
        """
        if self.verbose:
            print("Loading experimental data...")
        
        self.df_full = pd.read_csv(self.data_path)
        self.df_full = dfUtils(self.df_full)
        self.df_full.sanitize_old_df(inplace=True)
        
        if self.verbose:
            print(f"✓ Loaded {len(self.df_full)} experimental data points")
            print(f"  - Unique ILs: {self.df_full['sanitized_il_smiles'].nunique()}")
            print(f"  - Temperature range: {self.df_full['temperature_k'].min():.1f} - {self.df_full['temperature_k'].max():.1f} K")
            print()
        
        return self.df_full
    
    def set_il_from_smiles(self, 
                           cation_smiles: str, 
                           anion_smiles: str) -> str:
        """
        Set IL from cation and anion SMILES strings.
        
        Args:
            cation_smiles: SMILES string for cation
            anion_smiles: SMILES string for anion
        
        Returns:
            str: Sanitized IL SMILES
        """
        self.cation_smiles = cation_smiles
        self.anion_smiles = anion_smiles
        
        # Create combined SMILES
        self.il_smiles_original = f"{cation_smiles}.{anion_smiles}"
        self.il_smiles_sanitized = sanitized_smiles(self.il_smiles_original)
        
        if self.verbose:
            print(f"IL SMILES set: {self.il_smiles_sanitized}")
            print()
        
        return self.il_smiles_sanitized
    
    def query_il(self) -> pd.DataFrame:
        """
        Query experimental data for the current IL.
        
        Returns:
            pd.DataFrame: Query results for the IL
        
        Raises:
            ValueError: If no data found for IL or IL not set
        """
        if self.il_smiles_sanitized is None:
            raise ValueError("IL SMILES not set. Call set_il_from_smiles() first.")
        
        if self.df_full is None:
            self.load_experimental_data()
        
        self.df_query = self.df_full[self.df_full["sanitized_il_smiles"] == self.il_smiles_sanitized]
        
        if len(self.df_query) == 0:
            raise ValueError(f"No experimental data found for IL: {self.il_smiles_sanitized}")
        
        self.df_query = dfUtils(self.df_query)
        
        if self.verbose:
            print(f"Queried IL: {self.il_smiles_sanitized}")
            print(f"✓ Found {len(self.df_query)} experimental data points")
            print(f"  - Temperature range: {self.df_query['temperature_k'].min():.1f} - {self.df_query['temperature_k'].max():.1f} K")
            print(f"  - Viscosity range: {self.df_query['viscosity_mpas'].min():.2f} - {self.df_query['viscosity_mpas'].max():.2f} mPa·s")
            print()
        
        return self.df_query
    
    def create_prediction_inputs(self,
                                temperatures: Optional[List[float]] = None,
                                input_dir: str = "./model_input_files") -> Dict:
        """
        Create input files for GCNN prediction.
        
        Args:
            temperatures: List of temperatures for prediction. If None, uses experimental temperatures.
            input_dir: Directory to save input files
        
        Returns:
            Dict: Paths to created input files
        """
        if self.il_smiles_sanitized is None:
            raise ValueError("IL not set. Call set_il_from_smiles() and query_il() first.")
        
        # Use experimental temperatures if not specified
        if temperatures is None:
            temperatures = sorted(self.df_query['temperature_k'].unique().tolist())
        
        # Create SMILES list (same IL for all temperatures)
        il_smiles_list = [self.il_smiles_sanitized] * len(temperatures)
        
        if self.verbose:
            print(f"Creating prediction input files for {len(temperatures)} temperature points...")
        
        prediction_paths = create_chemprop_input_files(
            il_smiles=il_smiles_list,
            temperature_k=temperatures,
            input_files_dir=input_dir,
            verbose=self.verbose
        )
        
        return prediction_paths
    
    def run_prediction(self,
                       input_dir: str = "./model_input_files",
                       dry_run: bool = False) -> Dict:
        """
        Run GCNN prediction on prepared inputs.
        
        Args:
            input_dir: Directory containing input files
            dry_run: If True, only show command without executing
        
        Returns:
            Dict: Prediction results and execution info
        """
        if self.verbose and dry_run:
            print("Running in DRY-RUN mode (command only, no execution)")
        elif self.verbose:
            print("Running GCNN predictions...")
        
        result = run_chemprop_prediction(
            input_files_dir=input_dir,
            predict_script_path=str(self.predict_script_path),
            model_checkpoint_path=str(self.model_checkpoint_path),
            dry_run=dry_run,
            verbose=self.verbose
        )
        
        return result
    
    def load_and_compare(self,
                        predict_output_path: str = "./model_input_files/predict.csv") -> pd.DataFrame:
        """
        Load prediction results and compare with experimental data.
        
        Args:
            predict_output_path: Path to prediction CSV output
        
        Returns:
            pd.DataFrame: Comparison dataframe with errors
        """
        if self.df_query is None:
            raise ValueError("Query data not loaded. Call query_il() first.")
        
        if self.verbose:
            print("Loading and comparing prediction results...")
        
        # Load predictions
        self.df_results = process_chemprop_results(
            predict_output_path=predict_output_path,
            viscosity_format="log mpas"
        )
        
        # Convert to log scale
        self.df_results['log_10_pred_viscosity_mpas'] = np.log10(self.df_results['pred_0'])
        
        # Prepare dataframes for merging
        df_exp = self.df_query[['temperature_k', 'viscosity_mpas', 'log_10_viscosity_mpas']].copy()
        df_pred = self.df_results[['temperature_k', 'pred_0', 'log_10_pred_viscosity_mpas']].drop_duplicates().copy()
        
        # Merge with tolerance
        self.df_comparison = merge_with_tolerance(
            df_left=df_exp,
            df_right=df_pred,
            left_key='temperature_k',
            right_key='temperature_k',
            tolerance=self.temperature_tolerance,
            how='left'
        )
        
        # Calculate errors
        self.df_comparison['error'] = (self.df_comparison['log_10_pred_viscosity_mpas'] - 
                                        self.df_comparison['log_10_viscosity_mpas'])
        self.df_comparison['abs_error'] = np.abs(self.df_comparison['error'])
        self.df_comparison['percent_error'] = ((self.df_comparison['abs_error'] / 
                                                 self.df_comparison['log_10_viscosity_mpas']) * 100)
        
        if self.verbose:
            print(f"✓ Merged {len(self.df_comparison)} data points")
            print(f"\n=== Error Metrics ===")
            print(f"MAE (log units):        {self.df_comparison['abs_error'].mean():.4f}")
            print(f"RMSE (log units):       {np.sqrt((self.df_comparison['error']**2).mean()):.4f}")
            print(f"Max Error (log units):  {self.df_comparison['abs_error'].max():.4f}")
            print(f"Mean Percent Error:     {self.df_comparison['percent_error'].mean():.2f}%")
            print()
        
        return self.df_comparison
    
    def get_error_summary(self) -> Dict:
        """
        Get summary statistics of prediction errors.
        
        Returns:
            Dict: Error metrics (MAE, RMSE, max error, percent error)
        """
        if self.df_comparison is None:
            raise ValueError("Comparison data not available. Call load_and_compare() first.")
        
        return {
            'mae': self.df_comparison['abs_error'].mean(),
            'rmse': np.sqrt((self.df_comparison['error']**2).mean()),
            'max_error': self.df_comparison['abs_error'].max(),
            'mean_percent_error': self.df_comparison['percent_error'].mean(),
            'num_points': len(self.df_comparison)
        }
    
    def save_results(self, filename: str = "viscosity_comparison.csv") -> Path:
        """
        Save comparison results to CSV.
        
        Args:
            filename: Output filename
        
        Returns:
            Path: Path to saved file
        """
        if self.df_comparison is None:
            raise ValueError("Comparison data not available. Call load_and_compare() first.")
        
        output_path = self.output_dir / filename
        self.df_comparison.to_csv(output_path, index=False)
        
        if self.verbose:
            print(f"✓ Results saved to: {output_path}")
        
        return output_path
    
    def create_visualizations(self) -> Dict[str, Path]:
        """
        Create comprehensive analysis visualizations.
        
        Returns:
            Dict: Paths to saved figures
        """
        import matplotlib.pyplot as plt
        
        if self.df_comparison is None:
            raise ValueError("Comparison data not available. Call load_and_compare() first.")
        
        if self.verbose:
            print("Creating visualizations...")
        
        temperature_col = 'temperature_k'
        figures = {}
        
        # Style dictionary
        subset_styles = {
            'Experimental': {'marker': 'o', 'color': 'C0', 'label': 'Experimental',
                           's': 100, 'alpha': 0.7, 'edgecolors': 'blue', 'linewidth': 2},
            'Predicted': {'marker': '^', 'color': 'C1', 'label': 'Predicted',
                        's': 100, 'alpha': 0.7, 'edgecolors': 'red', 'linewidth': 2}
        }
        
        # === Figure 1: Comprehensive 4-subplot analysis ===
        fig, axes = plt.subplots(2, 2, figsize=(12, 10), dpi=150)
        fig.suptitle(f"GCNN Viscosity Prediction Analysis\nIL: {self.il_smiles_sanitized}",
                    fontsize=14, fontweight='bold')
        
        # Plot 1: Temperature vs Viscosity (linear)
        ax = axes[0, 0]
        ax.scatter(self.df_comparison[temperature_col], self.df_comparison['viscosity_mpas'],
                  **subset_styles['Experimental'])
        ax.scatter(self.df_comparison[temperature_col], self.df_comparison['pred_0'],
                  **subset_styles['Predicted'])
        ax.set_xlabel('Temperature (K)', fontsize=11)
        ax.set_ylabel('Viscosity (mPa·s)', fontsize=11)
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_title('Viscosity vs Temperature')
        
        # Plot 2: Temperature vs log Viscosity
        ax = axes[0, 1]
        ax.scatter(self.df_comparison[temperature_col], self.df_comparison['viscosity_mpas'],
                  **subset_styles['Experimental'])
        ax.scatter(self.df_comparison[temperature_col], self.df_comparison['pred_0'],
                  **subset_styles['Predicted'])
        ax.set_yscale('log')
        ax.set_xlabel('Temperature (K)', fontsize=11)
        ax.set_ylabel('log₁₀(Viscosity) [mPa·s]', fontsize=11)
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_title('log Viscosity vs Temperature')
        
        # Plot 3: Parity plot
        ax = axes[1, 0]
        min_val = min(self.df_comparison['log_10_viscosity_mpas'].min(),
                     self.df_comparison['log_10_pred_viscosity_mpas'].min())
        max_val = max(self.df_comparison['log_10_viscosity_mpas'].max(),
                     self.df_comparison['log_10_pred_viscosity_mpas'].max())
        ax.plot([min_val, max_val], [min_val, max_val], 'k--', lw=2, label='Perfect Prediction')
        ax.scatter(self.df_comparison['log_10_viscosity_mpas'],
                  self.df_comparison['log_10_pred_viscosity_mpas'],
                  **subset_styles['Predicted'])
        ax.set_xlabel('Experimental log₁₀(Viscosity) [mPa·s]', fontsize=11)
        ax.set_ylabel('Predicted log₁₀(Viscosity) [mPa·s]', fontsize=11)
        ax.legend()
        ax.grid(True, alpha=0.3)
        mae = self.df_comparison['abs_error'].mean()
        ax.set_title(f"Parity Plot (MAE: {mae:.4f})")
        
        # Plot 4: Error distribution
        ax = axes[1, 1]
        colors = ['green' if x > -0.5 else 'red' for x in self.df_comparison['error']]
        ax.bar(range(len(self.df_comparison)), self.df_comparison['error'], color=colors, alpha=0.7)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax.axhline(y=self.df_comparison['error'].mean(), color='blue', linestyle='--',
                  linewidth=2, label='Mean Error')
        ax.set_xlabel('Temperature Index', fontsize=11)
        ax.set_ylabel('Error (log units)', fontsize=11)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_title('Prediction Error by Temperature')
        
        plt.tight_layout()
        analysis_path = self.output_dir / "viscosity_analysis.png"
        fig.savefig(analysis_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        figures['analysis'] = analysis_path
        
        # === Figure 2: Simplified 2-subplot parity view ===
        fig, axes = plt.subplots(1, 2, figsize=(10, 5), dpi=150)
        fig.suptitle(f"GCNN Viscosity Prediction\nIL: {self.il_smiles_sanitized}",
                    fontsize=14, fontweight='bold')
        
        # Log viscosity vs temperature
        ax = axes[0]
        ax.scatter(self.df_comparison[temperature_col], self.df_comparison['viscosity_mpas'],
                  **subset_styles['Experimental'])
        ax.scatter(self.df_comparison[temperature_col], self.df_comparison['pred_0'],
                  **subset_styles['Predicted'])
        ax.set_yscale('log')
        ax.set_xlabel('Temperature (K)', fontsize=11)
        ax.set_ylabel('log₁₀(Viscosity) [mPa·s]', fontsize=11)
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_title('log Viscosity vs Temperature')
        
        # Parity plot
        ax = axes[1]
        min_val = min(self.df_comparison['log_10_viscosity_mpas'].min(),
                     self.df_comparison['log_10_pred_viscosity_mpas'].min())
        max_val = max(self.df_comparison['log_10_viscosity_mpas'].max(),
                     self.df_comparison['log_10_pred_viscosity_mpas'].max())
        ax.plot([min_val, max_val], [min_val, max_val], 'k--', lw=2, label='Perfect Prediction')
        ax.scatter(self.df_comparison['log_10_viscosity_mpas'],
                  self.df_comparison['log_10_pred_viscosity_mpas'],
                  **subset_styles['Predicted'])
        ax.set_xlabel('Experimental log₁₀(Viscosity) [mPa·s]', fontsize=11)
        ax.set_ylabel('Predicted log₁₀(Viscosity) [mPa·s]', fontsize=11)
        ax.legend()
        ax.grid(True, alpha=0.3)
        mae = self.df_comparison['abs_error'].mean()
        ax.set_title(f"Parity Plot (MAE: {mae:.4f})")
        
        plt.tight_layout()
        parity_path = self.output_dir / "viscosity_parity.png"
        fig.savefig(parity_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        figures['parity'] = parity_path
        
        if self.verbose:
            print(f"✓ Visualizations created:")
            for name, path in figures.items():
                print(f"  - {name}: {path}")
            print()
        
        return figures
    
    def run_full_workflow(self,
                         cation_smiles: str,
                         anion_smiles: str,
                         temperatures: Optional[List[float]] = None,
                         dry_run: bool = False) -> Dict:
        """
        Execute complete workflow from IL setup to visualization.
        
        Args:
            cation_smiles: Cation SMILES string
            anion_smiles: Anion SMILES string
            temperatures: Temperature points for prediction
            dry_run: If True, show command without executing
        
        Returns:
            Dict: Complete results and file paths
        """
        if self.verbose:
            print("\n" + "="*70)
            print("STARTING FULL IL VISCOSITY PREDICTION WORKFLOW")
            print("="*70 + "\n")
        
        try:
            # Step 1: Load data
            self.load_experimental_data()
            
            # Step 2: Set IL
            self.set_il_from_smiles(cation_smiles, anion_smiles)
            
            # Step 3: Query IL
            self.query_il()
            
            # Step 4: Create inputs
            prediction_paths = self.create_prediction_inputs(temperatures)
            
            # Step 5: Run prediction
            prediction_result = self.run_prediction(dry_run=dry_run)
            
            if dry_run:
                if self.verbose:
                    print("\n⚠️  Dry-run mode: Command shown but not executed")
                    print("   To run actual predictions, set dry_run=False")
                return {
                    'status': 'dry_run_complete',
                    'command': prediction_result.get('command'),
                    'message': 'Run workflow with dry_run=False to execute predictions'
                }
            
            # Step 6: Load and compare
            self.load_and_compare()
            
            # Step 7: Save results
            results_path = self.save_results()
            
            # Step 8: Create visualizations
            figures = self.create_visualizations()
            
            # Prepare final summary
            error_summary = self.get_error_summary()
            
            if self.verbose:
                print("="*70)
                print("WORKFLOW COMPLETE ✓")
                print("="*70)
            
            return {
                'status': 'success',
                'il_smiles': self.il_smiles_sanitized,
                'error_metrics': error_summary,
                'results_file': results_path,
                'figures': figures,
                'comparison_data': self.df_comparison
            }
        
        except Exception as e:
            if self.verbose:
                print(f"\n❌ Error in workflow: {str(e)}")
            raise
