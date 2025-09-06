from __future__ import annotations

import csv
import json
import os
from dataclasses import asdict, dataclass
from typing import Iterable, List, Optional, Tuple


def _import_rdkit():
	try:
		from rdkit import Chem
		from rdkit.Chem import AllChem, DataStructs
		return Chem, AllChem, DataStructs
	except Exception as e:
		raise RuntimeError("RDKit required for similarity tools") from e


@dataclass
class SimilarityHit:
	smiles: str
	name: Optional[str]
	score: float

	def to_dict(self):
		return asdict(self)



def _fp_from_smiles(smiles: str):
	Chem, AllChem, _ = _import_rdkit()
	mol = Chem.MolFromSmiles(smiles)
	if mol is None:
		raise ValueError(f"Invalid SMILES: {smiles}")
	return AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)



def tanimoto_similarity(smiles_a: str, smiles_b: str) -> str:
	Chem, AllChem, DataStructs = _import_rdkit()
	fp_a = _fp_from_smiles(smiles_a)
	fp_b = _fp_from_smiles(smiles_b)
	score = DataStructs.TanimotoSimilarity(fp_a, fp_b)
	return json.dumps({"tanimoto": round(float(score), 6)}, ensure_ascii=False)



def _load_dataset_rows(data_dir: str) -> Iterable[Tuple[str, Optional[str]]]:
	csv_path = os.path.join(data_dir, "molecules.csv")
	smi_path = os.path.join(data_dir, "molecules.smi")
	if os.path.exists(csv_path):
		with open(csv_path, "r", encoding="utf-8") as f:
			reader = csv.DictReader(f)
			for row in reader:
				yield row.get("smiles", "").strip(), (row.get("name") or None)
	elif os.path.exists(smi_path):
		with open(smi_path, "r", encoding="utf-8") as f:
			for line in f:
				parts = line.strip().split()
				if not parts:
					continue
				smi = parts[0]
				name = parts[1] if len(parts) > 1 else None
				yield smi, name
	else:
		raise FileNotFoundError("No dataset found at CHEMAGENT_DATA (molecules.csv or molecules.smi)")



def search_similar_in_dataset(query_smiles: str, top_k: int = 10) -> str:
	Chem, AllChem, DataStructs = _import_rdkit()
	data_dir = os.getenv("CHEMAGENT_DATA", os.path.join(os.getcwd(), "chemagent", "data"))
	query_fp = _fp_from_smiles(query_smiles)
	hits: List[SimilarityHit] = []
	for smi, name in _load_dataset_rows(data_dir):
		try:
			ref_fp = _fp_from_smiles(smi)
			score = DataStructs.TanimotoSimilarity(query_fp, ref_fp)
			hits.append(SimilarityHit(smiles=smi, name=name, score=float(score)))
		except Exception:
			continue
	hits.sort(key=lambda h: h.score, reverse=True)
	return json.dumps([h.to_dict() for h in hits[: top_k]], ensure_ascii=False)