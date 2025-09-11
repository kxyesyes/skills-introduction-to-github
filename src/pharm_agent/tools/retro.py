from typing import Dict, Any
import requests
from langchain.tools import tool

from ..config import CONFIG
from ..llm import get_chat_model, invoke_json
from ..prompts import DEFAULT_SYSTEM_PROMPT, RETRO_JSON_INSTRUCTIONS
from ..schemas import RetroPlan
import json


def _external_retro(target: str) -> Dict[str, Any] | None:
    if not CONFIG.retro_api_url:
        return None
    try:
        resp = requests.post(CONFIG.retro_api_url, json={"target": target}, timeout=60)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


def _llm_retro(target: str) -> RetroPlan:
    chat = get_chat_model()
    system = f"{DEFAULT_SYSTEM_PROMPT}\n\nTask: Propose retrosynthetic routes."
    user = f"Target: {target}\n\n{RETRO_JSON_INSTRUCTIONS}"
    text = invoke_json(chat, system, user)
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
    return RetroPlan(**data)


@tool("retrosynthesis", return_direct=False)
def retrosynthesis(target: str) -> Dict[str, Any]:
    """Recommend retrosynthetic routes for a target product. Output follows RetroPlan schema."""
    external = _external_retro(target)
    if external is not None:
        try:
            plan = RetroPlan(**external)
            return {"source": "external", "result": plan.model_dump()}
        except Exception:
            return {"source": "external", "raw": external}
    plan = _llm_retro(target)
    return {"source": "llm", "result": plan.model_dump()}


def make_retro_tool():
    return retrosynthesis

