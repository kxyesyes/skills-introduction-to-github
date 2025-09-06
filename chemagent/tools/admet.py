from __future__ import annotations

import json
import os
from typing import Dict, Any

from .properties import calculate_properties

import requests


def _heuristic_admet(smiles: str) -> Dict[str, Any]:
	props = json.loads(calculate_properties(smiles))
	mw = props["mw"]
	logp = props["logp"]
	tpsa = props["tpsa"]
	hbd = props["hbd"]
	hba = props["hba"]
	rot = props["rot_bonds"]

	# Very rough heuristics inspired by drug-likeness filters
	absorption = "high" if (logp <= 5 and tpsa < 120 and rot <= 10) else "moderate" if tpsa < 150 else "low"
	distribution = "moderate" if (logp <= 3 and mw < 500) else "high" if logp > 3 else "low"
	metabolism = "moderate" if logp > 2 else "low"
	toxicity = "low" if (mw < 600 and hbd <= 5 and hba <= 10) else "moderate"

	return {
		"absorption": absorption,
		"distribution": distribution,
		"metabolism": metabolism,
		"excretion": "unknown",
		"toxicity": toxicity,
		"notes": "Heuristic estimate. Provide ADMET_API_URL for model-backed predictions.",
	}


def predict_admet(smiles: str) -> str:
	api = os.getenv("ADMET_API_URL")
	if api:
		try:
			resp = requests.post(api, json={"smiles": smiles}, timeout=30)
			resp.raise_for_status()
			return json.dumps(resp.json(), ensure_ascii=False)
		except Exception as e:
			# fallback
			fallback = _heuristic_admet(smiles)
			fallback["warning"] = f"External ADMET call failed: {e}"
			return json.dumps(fallback, ensure_ascii=False)
	else:
		return json.dumps(_heuristic_admet(smiles), ensure_ascii=False)