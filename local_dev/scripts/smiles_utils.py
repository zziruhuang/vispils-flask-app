import rdkit
from rdkit import Chem  

def sanitized_smiles(smiles: str) -> str:
    """
    Convert a SMILES string to its canonical, sanitized form.
    
    Args:
        smiles: SMILES string to sanitize
        
    Returns:
        Sanitized SMILES string in canonical form and include information about stereochemistry (isomericSmiles=True).
        
    Raises:
        ValueError: If SMILES string is invalid or None
    """
    if not smiles or not isinstance(smiles, str):
        raise ValueError(f"Invalid SMILES input: {smiles}. Must be a non-empty string.")
    
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            raise ValueError(f"RDKit could not parse SMILES: {smiles}")
        return Chem.MolToSmiles(mol, isomericSmiles=True, canonical=True)
    except Exception as e:
        raise ValueError(f"Error sanitizing SMILES '{smiles}': {str(e)}")