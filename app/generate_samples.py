"""
Generate Sample Molecular Images
===============================

This script generates sample molecular images for cations and anions
and saves them as static assets for the frontend.

Author: Ziru Huang
Date: 2025-07-07
"""

import os
import sys
from rdkit import Chem
from rdkit.Chem import Draw
from PIL import Image

# Add the backend directory to the path
sys.path.append(os.path.dirname(__file__))

def generate_molecular_image(smiles, filename, output_dir, size=(300, 300)):
    """
    Generate a molecular image from SMILES and save it as PNG with transparent background.
    
    Args:
        smiles (str): SMILES string
        filename (str): Output filename
        output_dir (str): Output directory
        size (tuple): Image size (width, height)
    """
    try:
        # Create molecule from SMILES
        mol = Chem.MolFromSmiles(smiles)
        iso_smis = Chem.MolToSmiles(mol, isomericSmiles=True)

        if mol is None:
            print(f"Error: Could not create molecule from SMILES: {smiles}")
            return False
        
        # Generate image (RGB)
        img = Draw.MolToImage(mol, size=size)
        # Convert to RGBA
        img = img.convert("RGBA")
        datas = img.getdata()
        newData = []
        for item in datas:
            # Replace white background with transparency
            if item[0] > 240 and item[1] > 240 and item[2] > 240:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        img.putdata(newData)
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Save image
        output_path = os.path.join(output_dir, filename)
        img.save(output_path, "PNG")
        print(f"✓ Generated: {output_path}")
        print(f" Iso SMILES: {iso_smis}")

        return True
        
    except Exception as e:
        print(f"Error generating image for {smiles}: {e}")
        return False

def main():
    """Generate sample molecular images."""
    
    # Define sample molecules
    sample_cations = {
        "CCn1cc[n+](C)c1": "sample_cation_1.png",  # 1-butyl-3-methylimidazolium
        "CCCC[N+](C)(CC)CC": "sample_cation_2.png",  # N,N-diethyl-N-methyl-N-(n-butyl)ammonium
        "CCCC[n+]1ccncc1": "sample_cation_3.png",  # 1-butyl-3-methylpyrazolium
    }
    
    sample_anions = {
        "F[B-](F)(F)F": "sample_anion_1_bf4.png",  # Tetrafluoroborate
        "F[P-](F)(F)(F)(F)F": "sample_anion_2_pf6.png",  # Trifluoromethanesulfonate
        "O=S(=O)([N-]S(=O)(=O)C(F)(F)F)C(F)(F)F": "sample_anion_3_tf2n.png",  # Bis(trifluoromethanesulfonyl)imide
    }
    
    # Output directory (frontend static assets)
    output_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "static", "img", "samples")
    
    print("Generating Sample Molecular Images...")
    print("=" * 50)
    
    # Generate cation images
    print("\n📊 Generating Cation Images:")
    cation_success = 0
    for smiles, filename in sample_cations.items():
        if generate_molecular_image(smiles, filename, output_dir):
            cation_success += 1
    
    # Generate anion images
    print("\n📊 Generating Anion Images:")
    anion_success = 0
    for smiles, filename in sample_anions.items():
        if generate_molecular_image(smiles, filename, output_dir):
            anion_success += 1
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print(f"Cations generated: {cation_success}/{len(sample_cations)}")
    print(f"Anions generated: {anion_success}/{len(sample_anions)}")
    print(f"Total: {cation_success + anion_success}/{len(sample_cations) + len(sample_anions)}")
    
    if cation_success + anion_success == len(sample_cations) + len(sample_anions):
        print("\n✅ All images generated successfully!")
        print(f"📁 Images saved to: {output_dir}")
    else:
        print("\n⚠️  Some images failed to generate. Check the errors above.")

if __name__ == "__main__":
    main() 