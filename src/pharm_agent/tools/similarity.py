from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Iterable
import os
import pandas as pd
from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem
from langchain.tools import tool


def _mol_from_smiles(smiles: str):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError("Invalid SMILES")
    return mol


def _fp_from_mol(mol):
    return AllChem.GetMorganFingerprintAsBitVect(mol, radius=2, nBits=2048)


@dataclass
class SimilarityIndex:
    smiles_list: List[str]
    fps: List

    @classmethod
    def from_csv(cls, path: str, smiles_col: str = "smiles") -> "SimilarityIndex":
        df = pd.read_csv(path)
        smiles_list = df[smiles_col].dropna().astype(str).tolist()
        fps = [_fp_from_mol(_mol_from_smiles(s)) for s in smiles_list]
        return cls(smiles_list=smiles_list, fps=fps)

    def search(self, query_smiles: str, top_k: int = 10) -> List[Tuple[str, float]]:
        qmol = _mol_from_smiles(query_smiles)
        qfp = _fp_from_mol(qmol)
        scores = [DataStructs.TanimotoSimilarity(qfp, fp) for fp in self.fps]
        ranked = sorted(zip(self.smiles_list, scores), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]


def _default_dataset_path() -> str:
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "dataset", "sample_mols.csv")


def make_similarity_tool(index: SimilarityIndex | None = None):
    idx = index or SimilarityIndex.from_csv(_default_dataset_path())

    @tool("similarity_search", return_direct=False)
    def similarity_search(smiles: str, top_k: int = 10):
        """Compute Tanimoto similarity in local dataset and return top_k similar SMILES."""
        return {"query": smiles, "results": idx.search(smiles, top_k=top_k)}

    return similarity_search

