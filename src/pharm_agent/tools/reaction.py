from typing import Dict, Any
import requests
from langchain.tools import tool

from ..config import CONFIG
from ..llm import get_chat_model, invoke_json
from ..prompts import DEFAULT_SYSTEM_PROMPT, REACTION_JSON_INSTRUCTIONS
from ..schemas import ReactionPrediction, ReactionProduct, ReactionCondition
import json


def _external_reaction(reactants: str) -> Dict[str, Any] | None:
    if not CONFIG.reaction_api_url:
        return None
    try:
        resp = requests.post(CONFIG.reaction_api_url, json={"reactants": reactants}, timeout=60)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


def _llm_reaction(reactants: str) -> ReactionPrediction:
    chat = get_chat_model()
    system = f"{DEFAULT_SYSTEM_PROMPT}\n\nTask: Predict reaction products."
    user = f"Reactants: {reactants}\n\n{REACTION_JSON_INSTRUCTIONS}"
    text = invoke_json(chat, system, user)
    # Try to parse JSON strictly; fallback to extracting braces
    def _parse(payload: str) -> Dict[str, Any]:
        try:
            return json.loads(payload)
        except Exception:
            start = payload.find("{")
            end = payload.rfind("}")
            if start != -1 and end != -1 and end > start:
                return json.loads(payload[start : end + 1])
            raise
    data = _parse(text)
    # Validate and coerce into schema
    pred = ReactionPrediction(**data)
    return pred


@tool("reaction_predict", return_direct=False)
def reaction_predict(reactants: str) -> Dict[str, Any]:
    """Predict reaction products from reactants string (SMILES or names). Output follows ReactionPrediction schema."""
    external = _external_reaction(reactants)
    if external is not None:
        # Attempt to normalize external into schema; if not possible, wrap
        try:
            pred = ReactionPrediction(**external)
            return {"source": "external", "result": pred.model_dump()}
        except Exception:
            return {"source": "external", "raw": external}
    pred = _llm_reaction(reactants)
    return {"source": "llm", "result": pred.model_dump()}


def make_reaction_tool():
    return reaction_predict

