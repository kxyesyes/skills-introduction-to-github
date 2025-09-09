from typing import Dict, Any
import requests
from langchain.tools import tool
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

from ..config import CONFIG


def _heuristic_admet(smiles: str) -> Dict[str, Any]:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError("Invalid SMILES")
    mw = rdMolDescriptors.CalcExactMolWt(mol)
    hbd = rdMolDescriptors.CalcNumHBD(mol)
    hba = rdMolDescriptors.CalcNumHBA(mol)
    tpsa = rdMolDescriptors.CalcTPSA(mol)
    rot = rdMolDescriptors.CalcNumRotatableBonds(mol)

    rules = []
    lipinski = (mw <= 500) and (hbd <= 5) and (hba <= 10) and (tpsa <= 140) and (rot <= 10)
    rules.append({"rule": "Lipinski-like", "pass": lipinski})
    # Simple TPSA-based permeability heuristic
    permeability = "high" if tpsa < 60 else ("moderate" if tpsa < 120 else "low")
    # Simple MW-based distribution heuristic
    vd_heur = "wide" if mw < 350 else ("moderate" if mw < 600 else "limited")

    return {
        "smiles": smiles,
        "heuristics": {
            "absorption_permeability": permeability,
            "distribution_volume": vd_heur,
            "metabolism_risk": "moderate" if rot > 7 else "low",
            "excretion_rate": "faster" if mw < 350 else "slower",
            "toxicity_risk": "elevated" if tpsa < 20 else "unknown",
        },
        "rule_checks": rules,
        "descriptors": {"mw": mw, "hbd": hbd, "hba": hba, "tpsa": tpsa, "rotatable_bonds": rot},
    }


def _external_admet(smiles: str) -> Dict[str, Any] | None:
    if not CONFIG.admet_api_url:
        return None
    try:
        resp = requests.post(CONFIG.admet_api_url, json={"smiles": smiles}, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


@tool("admet_predict", return_direct=False)
def admet_predict(smiles: str) -> Dict[str, Any]:
    """Predict ADMET properties for a SMILES string using heuristics or an external API if configured."""
    external = _external_admet(smiles)
    if external is not None:
        return {"smiles": smiles, "source": "external", "result": external}
    return {"smiles": smiles, "source": "heuristic", "result": _heuristic_admet(smiles)}


def make_admet_tool():
    return admet_predict

