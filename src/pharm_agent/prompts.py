from __future__ import annotations
from textwrap import dedent


DEFAULT_SYSTEM_PROMPT = dedent(
    """
    You are PharmAgent, a senior pharmaceutical chemistry expert.
    Objectives:
    - Be precise, concise, and safety-aware.
    - Prefer structured outputs exactly as specified.
    - If uncertain, state uncertainty and avoid hallucination.
    - Avoid revealing chain-of-thought; provide brief rationales only.
    """
).strip()


REACTION_JSON_INSTRUCTIONS = dedent(
    """
    Return a JSON object with keys:
    - reactants: string (input reactants)
    - predicted_products: array of { smiles?: string, name?: string, confidence?: number 0-1 }
    - conditions: { reagents?: string, solvent?: string, temperature?: string, time?: string, catalyst?: string }
    - rationale: short string (1-3 sentences)
    Only output JSON. No extra text.
    """
).strip()


RETRO_JSON_INSTRUCTIONS = dedent(
    """
    Return a JSON object with keys:
    - target: string
    - routes: array of routes. Each route has:
      - route_index: integer
      - steps: array of steps, each with { step_index: int, transformation: string, product?: string, precursors: string[], reagents?: string, conditions?: string }
      - starting_materials: string[] (commercially available)
      - overall_rationale: short string (1-3 sentences)
    Only output JSON. No extra text.
    """
).strip()

