from __future__ import annotations

import json
import os
from typing import Any, Dict, List

import requests


def _heuristic_retro(product_smiles: str) -> Dict[str, Any]:
	# Minimal placeholder that suggests disconnections
	return {
		"target": product_smiles,
		"routes": [
			{"steps": [
				{"reaction": "Disconnection heuristic", "starting_materials": ["<model_required>"]}
			]},
		],
		"notes": "Provide RETRO_API_URL for model-backed retrosynthesis.",
	}


def retrosynthesis_routes(product_smiles: str) -> str:
	api = os.getenv("RETRO_API_URL")
	if api:
		try:
			resp = requests.post(api, json={"product": product_smiles}, timeout=120)
			resp.raise_for_status()
			return json.dumps(resp.json(), ensure_ascii=False)
		except Exception as e:
			fallback = _heuristic_retro(product_smiles)
			fallback["warning"] = f"External retrosynthesis API failed: {e}"
			return json.dumps(fallback, ensure_ascii=False)
	else:
		return json.dumps(_heuristic_retro(product_smiles), ensure_ascii=False)