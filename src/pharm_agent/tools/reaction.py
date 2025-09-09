from typing import Dict, Any
import requests
from langchain.tools import tool

from ..config import CONFIG
from ..llm import get_chat_model


def _external_reaction(reactants: str) -> Dict[str, Any] | None:
    if not CONFIG.reaction_api_url:
        return None
    try:
        resp = requests.post(CONFIG.reaction_api_url, json={"reactants": reactants}, timeout=60)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


def _llm_reaction(reactants: str) -> Dict[str, Any]:
    chat = get_chat_model()
    system = (
        "You are a synthetic chemistry assistant. Given reactants in SMILES or names, "
        "propose likely major product(s) with brief rationale. Output JSON with keys: products (list of SMILES or names), rationale."
    )
    prompt = f"Reactants: {reactants}"
    res = chat.invoke([{"role": "system", "content": system}, {"role": "user", "content": prompt}])
    text = res.content if hasattr(res, "content") else str(res)
    return {"products_text": text}


@tool("reaction_predict", return_direct=False)
def reaction_predict(reactants: str) -> Dict[str, Any]:
    """Predict reaction products from reactants string (SMILES or names). Uses external API if available, else LLM heuristic."""
    external = _external_reaction(reactants)
    if external is not None:
        return {"source": "external", "result": external}
    return {"source": "llm", "result": _llm_reaction(reactants)}


def make_reaction_tool():
    return reaction_predict

