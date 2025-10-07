"""
VISPILS Backend Flask Application
================================

A Flask web application for ionic liquid property prediction and molecular visualization.
Provides APIs for:
- Molecular structure visualization (2D/3D)
- Ionic liquid selection and property prediction
- Data retrieval from VISPILS database

Author: Ziru Huang
Date: 2025
"""

import os
import base64
import io
import numpy as np
import pandas as pd

from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS

from rdkit import Chem
from rdkit.Chem import Draw
from PIL import Image
from openbabel import pybel

# Import prediction modules (uncomment when available)
# from vispils.predict import process_int, assign_g2cnn_descs, get_gcnn_files


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def smiles_to_base64(smiles):
    """
    Convert SMILES string to base64 encoded PNG image.
    
    Args:
        smiles (str): SMILES molecular representation
        
    Returns:
        str: Base64 encoded PNG image data
    """
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        
        img_pil = Draw.MolToImage(mol)
        buffer = io.BytesIO()
        img_pil.save(buffer, format="PNG")
        encoded_img_data = base64.b64encode(buffer.getvalue())
        return encoded_img_data.decode('utf-8')
    except Exception as e:
        print(f"Error converting SMILES to image: {e}")
        return None


def smiles_to_3d_molfile(smiles):
    """
    Convert SMILES string to 3D MOL file format.
    
    Args:
        smiles (str): SMILES molecular representation
        
    Returns:
        str: MOL file content with 3D coordinates
    """
    try:
        mol = pybel.readstring("smi", smiles)
        mol.addh()
        mol.make3D()
        return mol.write('mol')
    except Exception as e:
        print(f"Error converting SMILES to 3D MOL: {e}")
        return None


def load_vispils_data():
    """
    Load and prepare VISPILS database data.
    
    Returns:
        tuple: (vispils_df, cations_df, anions_df)
    """
    try:
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "vispils-v1.csv")
        vispils_df = pd.read_csv(data_path)
        
        # Extract unique cations and anions
        cations_df = vispils_df.drop_duplicates(['cSMILES'])[['cSMILES', 'cfam1', 'cfam_class']]
        anions_df = vispils_df.drop_duplicates(['aSMILES'])[['aSMILES', 'afam1', 'afam_class']]
        
        return vispils_df, cations_df, anions_df
    except Exception as e:
        print(f"Error loading VISPILS data: {e}")
        return None, None, None


# =============================================================================
# FLASK APPLICATION SETUP
# =============================================================================

app = Flask(__name__, 
            template_folder='../frontend/templates', 
            static_folder='../frontend/static')

# Enable CORS for frontend integration
CORS(app)

# Load data
VISPILS_DATA, CATIONS_DATA, ANIONS_DATA = load_vispils_data()

# Global user selection storage (in production, use Redis or database)
user_selections = {}


# =============================================================================
# ROUTES
# =============================================================================

@app.route('/')
def home():
    """Main landing page."""
    user_selections.clear()  # Clear previous selections
    return render_template('index.html')


@app.route('/api/selection', methods=['POST'])
def handle_selection():
    """
    Handle ionic liquid component selection.
    
    Expected JSON payload:
    {
        "select-cfams": "family_name" | "select-afams": "family_name" | "select-cations": "smiles" | "select-anions": "smiles"
    }
    
    Returns:
        JSON: List of candidate molecules with images
    """
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        
        req_data = request.get_json()
        if not req_data:
            return jsonify({"error": "Empty request data"}), 400
        
        # Extract selection type and value
        selection_type = list(req_data.keys())[0]
        selection_value = list(req_data.values())[0]
        
        # Store user selection
        user_selections[selection_type] = selection_value
        
        # Handle different selection types
        if selection_type == 'select-cfams':
            # Get cations from selected cation family
            candidates = CATIONS_DATA[CATIONS_DATA['cfam1'] == selection_value]['cSMILES'].tolist()
            
        elif selection_type == 'select-afams':
            # Get anions from selected anion family
            candidates = ANIONS_DATA[ANIONS_DATA['afam_class'] == selection_value]['aSMILES'].tolist()
            
        elif selection_type in ['select-cations', 'select-anions']:
            # Direct SMILES selection - return success
            return jsonify({"success": True, "message": f"{selection_type} selected"}), 200
        
        else:
            return jsonify({"error": f"Unknown selection type: {selection_type}"}), 400
        
        # Generate images for candidates
        candidates_data = []
        for smiles in candidates:
            img_base64 = smiles_to_base64(smiles)
            if img_base64:
                candidates_data.append({
                    "smiles": smiles,
                    "image_url": f"data:image/png;base64,{img_base64}"
                })
        
        return jsonify({
            "success": True,
            "candidates": candidates_data,
            "count": len(candidates_data)
        }), 200
        
    except Exception as e:
        print(f"Error in selection handler: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/ionic-liquid', methods=['POST'])
def create_ionic_liquid():
    """
    Create ionic liquid from selected cation and anion.
    
    Expected JSON payload:
    {
        "select-cations": "cation_smiles",
        "select-anions": "anion_smiles"
    }
    
    Returns:
        JSON: Ionic liquid data including 3D structure
    """
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        
        req_data = request.get_json()
        cation_smiles = req_data.get('select-cations')
        anion_smiles = req_data.get('select-anions')
        
        if not cation_smiles or not anion_smiles:
            return jsonify({"error": "Both cation and anion SMILES required"}), 400
        
        # Create ionic liquid SMILES
        ionic_liquid_smiles = f"{cation_smiles}.{anion_smiles}"
        
        # Generate 3D structure
        molfile_3d = smiles_to_3d_molfile(ionic_liquid_smiles)
        
        return jsonify({
            "success": True,
            "ionic_liquid": {
                "smiles": ionic_liquid_smiles,
                "cation": cation_smiles,
                "anion": anion_smiles,
                "molfile_3d": molfile_3d
            }
        }), 200
        
    except Exception as e:
        print(f"Error creating ionic liquid: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/predict', methods=['POST'])
def predict_properties():
    """
    Predict ionic liquid properties.
    
    Expected form data:
    - SMILES_input: Ionic liquid SMILES
    - Temperature_input: Temperature in Kelvin
    
    Returns:
        JSON: Predicted properties
    """
    try:
        # Get input data
        smiles_input = request.form.get('SMILES_input')
        temperature_input = request.form.get('Temperature_input')
        
        if not smiles_input or not temperature_input:
            return jsonify({"error": "SMILES and temperature required"}), 400
        
        # Convert temperature to float
        try:
            temperature = float(temperature_input)
        except ValueError:
            return jsonify({"error": "Invalid temperature value"}), 400
        
        # Standardize SMILES
        try:
            mol = Chem.MolFromSmiles(smiles_input)
            if mol is None:
                return jsonify({"error": "Invalid SMILES string"}), 400
            standardized_smiles = Chem.MolToSmiles(mol, isomericSmiles=True)
        except Exception as e:
            return jsonify({"error": f"Error processing SMILES: {e}"}), 400
        
        # Search in VISPILS database
        tolerance = 0.15
        matching_data = VISPILS_DATA[
            (VISPILS_DATA['Iso SMILES'] == standardized_smiles) & 
            (VISPILS_DATA['Temperature'].between(temperature - tolerance, temperature + tolerance))
        ]

        experimental_value = None
        experimental_text = None
        if len(matching_data) >= 1:
            # Found in database
            row = matching_data.iloc[0]
            experimental_value = 10 ** row['Log viscosity']
            experimental_text = f'η = {experimental_value:.2f} mPas at {temperature} K (Experimental)'
        
        # Always run ML prediction
        predicted_value = None
        predicted_text = None
        try:
            smis_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'data-smis.csv')
            descs_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'data-descs.csv')
            predict_out_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'Predict.csv')
            with open(smis_path, 'w') as f:
                f.write('Iso SMILES,Log viscosity\n')
                f.write(f'{standardized_smiles},0\n')
            with open(descs_path, 'w') as f:
                f.write('temperature\n')
                f.write(f'{temperature}\n')
            import subprocess
            script_path = os.path.join(os.path.dirname(__file__), '..', 'vispils', 'predict.py')
            checkpoint_path = os.path.join(os.path.dirname(__file__), '..', 'vispils', 'model', 'model-corr-5-temp-100-3-2-scale3-constrain-seed42', 'fold_0')
            cmd = [
                'python', script_path,
                '--data_path', smis_path,
                '--features_path', descs_path,
                '--checkpoint_path', checkpoint_path,
                '--save_dir', os.path.dirname(predict_out_path),
                '--hidden_size', '100',
                '--no_cuda'
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            print("Prediction script STDOUT:\n", result.stdout)
            print("Prediction script STDERR:\n", result.stderr)
            if result.returncode == 0:
                import csv
                with open(predict_out_path, 'r') as f:
                    reader = csv.reader(f)
                    header = next(reader)
                    pred_row = next(reader)
                    log_viscosity = float(pred_row[-1])
                    predicted_value = np.exp(log_viscosity)
                    predicted_text = f'η = {predicted_value:.2f} mPas at {temperature} K (Predicted)'
            else:
                print('Prediction script error:', result.stderr)
        except Exception as e:
            print(f"Error running ML prediction: {e}")

        # Compose output for both values
        output = {
            "standardized_smiles": standardized_smiles,
            "temperature": temperature,
            "experimental_value": experimental_value,
            "experimental_text": experimental_text,
            "predicted_value": predicted_value,
            "predicted_text": predicted_text
        }
        return jsonify({
            "success": True,
            "prediction": output
        }), 200
        
    except Exception as e:
        print(f"Error in prediction: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/molfile3d', methods=['POST'])
def molfile3d():
    """
    Generate a 3D MOL file from a SMILES string.
    Expected JSON payload:
    {
        "smiles": "CCO"
    }
    Returns:
        JSON: { "success": True, "molfile_3d": "..." }
    """
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        req_data = request.get_json()
        smiles = req_data.get('smiles')
        if not smiles:
            return jsonify({"error": "SMILES string required"}), 400
        molfile_3d = smiles_to_3d_molfile(smiles)
        if not molfile_3d:
            return jsonify({"error": "Failed to generate 3D structure"}), 500
        return jsonify({"success": True, "molfile_3d": molfile_3d}), 200
    except Exception as e:
        print(f"Error in /api/molfile3d: {e}")
        return jsonify({"error": "Internal server error"}), 500


# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500


# =============================================================================
# APPLICATION ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    # Check if data is loaded
    if VISPILS_DATA is None:
        print("ERROR: Could not load VISPILS data. Please check the data file.")
        exit(1)
    
    print("VISPILS Backend Server Starting...")
    print(f"Loaded {len(VISPILS_DATA)} ionic liquid records")
    print(f"Available cation families: {len(CATIONS_DATA['cfam1'].unique())}")
    print(f"Available anion families: {len(ANIONS_DATA['afam_class'].unique())}")
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5001)