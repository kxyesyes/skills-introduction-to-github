from typing import Dict, Any
import requests
from langchain.tools import tool

from ..config import CONFIG
from ..llm import get_chat_model


def _external_retro(target: str) -> Dict[str, Any] | None:
    if not CONFIG.retro_api_url:
        return None
    try:
        resp = requests.post(CONFIG.retro_api_url, json={"target": target}, timeout=60)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


def _llm_retro(target: str) -> Dict[str, Any]:
    chat = get_chat_model()
    system = (
        "You are a retrosynthesis planner. Given a target product (SMILES or name), propose 2-3 stepwise synthetic routes, with reagents and conditions. "
        "Prefer commercially available starting materials. Output concise bullet points."
    )
    prompt = f"Target: {target}"
    res = chat.invoke([{"role": "system", "content": system}, {"role": "user", "content": prompt}])
    text = res.content if hasattr(res, "content") else str(res)
    return {"routes_text": text}


@tool("retrosynthesis", return_direct=False)
def retrosynthesis(target: str) -> Dict[str, Any]:
    """Recommend retrosynthetic routes for a target product (SMILES or name). Uses external API if configured, else LLM heuristic."""
    external = _external_retro(target)
    if external is not None:
        return {"source": "external", "result": external}
    return {"source": "llm", "result": _llm_retro(target)}


def make_retro_tool():
    return retrosynthesis

