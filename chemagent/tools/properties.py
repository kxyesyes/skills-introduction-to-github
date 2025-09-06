from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any, Dict


def _import_rdkit():
	try:
		from rdkit import Chem
		from rdkit.Chem import Descriptors, rdMolDescriptors, Crippen, Lipinski
		return Chem, Descriptors, rdMolDescriptors, Crippen, Lipinski
	except Exception as e:  # pragma: no cover
		raise RuntimeError(
			"RDKit import failed. Please install rdkit-pypi and ensure compatible Python."
		) from e


@dataclass
class MolecularProperties:
	mw: float
	logp: float
	tpsa: float
	hbd: int
	hba: int
	rot_bonds: int
	heavy_atoms: int
	fraction_csp3: float
	formula: str

	def to_json(self) -> str:
		return json.dumps(asdict(self), ensure_ascii=False)



def _smiles_to_mol(smiles: str):
	Chem, *_ = _import_rdkit()
	mol = Chem.MolFromSmiles(smiles)
	if mol is None:
		raise ValueError(f"Invalid SMILES: {smiles}")
	return mol



def calculate_properties(smiles: str) -> str:
	"""Return JSON string with core molecular properties for a SMILES string."""
	Chem, Descriptors, rdMolDescriptors, Crippen, Lipinski = _import_rdkit()
	mol = _smiles_to_mol(smiles)
	mw = Descriptors.MolWt(mol)
	logp = Crippen.MolLogP(mol)
	tpsa = rdMolDescriptors.CalcTPSA(mol)
	hbd = Lipinski.NumHDonors(mol)
	hba = Lipinski.NumHAcceptors(mol)
	rot_bonds = Lipinski.NumRotatableBonds(mol)
	heavy_atoms = Descriptors.HeavyAtomCount(mol)
	fraction_csp3 = rdMolDescriptors.CalcFractionCSP3(mol)
	formula = rdMolDescriptors.CalcMolFormula(mol)
	props = MolecularProperties(
		mw=round(mw, 4),
		logp=round(logp, 4),
		tpsa=round(tpsa, 4),
		hbd=int(hbd),
		hba=int(hba),
		rot_bonds=int(rot_bonds),
		heavy_atoms=int(heavy_atoms),
		fraction_csp3=round(fraction_csp3, 4),
		formula=formula,
	)
	return props.to_json()