from __future__ import annotations

import json
import os
from typing import Any, Dict

import requests


def _heuristic_reaction_predict(reactants: str) -> Dict[str, Any]:
	# Simple placeholder: echo input and provide a generic note
	return {
		"reactants": reactants,
		"predicted_products": ["<model_required>"],
		"notes": "Provide REACTION_API_URL for model-backed predictions.",
	}


def predict_reaction_products(reactants_smiles: str) -> str:
	# Reactants separated by '.' similar to RDKit style
	api = os.getenv("REACTION_API_URL")
	if api:
		try:
			resp = requests.post(api, json={"reactants": reactants_smiles}, timeout=60)
			resp.raise_for_status()
			return json.dumps(resp.json(), ensure_ascii=False)
		except Exception as e:
			fallback = _heuristic_reaction_predict(reactants_smiles)
			fallback["warning"] = f"External reaction API failed: {e}"
			return json.dumps(fallback, ensure_ascii=False)
	else:
		return json.dumps(_heuristic_reaction_predict(reactants_smiles), ensure_ascii=False)