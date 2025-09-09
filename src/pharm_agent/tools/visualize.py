from typing import Optional
from langchain.tools import tool
from rdkit import Chem
from rdkit.Chem import Draw


@tool("draw_molecule", return_direct=False)
def draw_molecule(smiles: str, out_path: str = "molecule.png", size: int = 300) -> str:
    """Render a SMILES to an image file. Returns output path."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError("Invalid SMILES")
    img = Draw.MolToImage(mol, size=(size, size))
    img.save(out_path)
    return out_path


def make_draw_tool():
    return draw_molecule

