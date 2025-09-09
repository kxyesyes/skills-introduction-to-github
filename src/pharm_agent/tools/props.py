from typing import Dict, Any
from langchain.tools import tool
from rdkit import Chem
from rdkit.Chem import Descriptors, Crippen, rdMolDescriptors


def _mol_from_smiles(smiles: str):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError("Invalid SMILES string")
    return mol


def calc_basic_properties(smiles: str) -> Dict[str, Any]:
    mol = _mol_from_smiles(smiles)
    return {
        "smiles": smiles,
        "formula": rdMolDescriptors.CalcMolFormula(mol),
        "molecular_weight": Descriptors.MolWt(mol),
        "logp": Crippen.MolLogP(mol),
        "tpsa": rdMolDescriptors.CalcTPSA(mol),
        "hbd": rdMolDescriptors.CalcNumHBD(mol),
        "hba": rdMolDescriptors.CalcNumHBA(mol),
        "rotatable_bonds": rdMolDescriptors.CalcNumRotatableBonds(mol),
        "rings": rdMolDescriptors.CalcNumRings(mol),
    }


@tool("molecular_properties", return_direct=False)
def molecular_properties(smiles: str) -> Dict[str, Any]:
    """Compute RDKit molecular properties for a SMILES string: MW, LogP, TPSA, HBD/HBA, etc."""
    return calc_basic_properties(smiles)


def make_props_tool():
    return molecular_properties

