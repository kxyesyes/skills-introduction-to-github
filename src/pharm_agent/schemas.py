from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field


class ReactionProduct(BaseModel):
    smiles: Optional[str] = Field(None, description="Product SMILES if available")
    name: Optional[str] = Field(None, description="Product name if SMILES unknown")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)


class ReactionCondition(BaseModel):
    reagents: Optional[str] = None
    solvent: Optional[str] = None
    temperature: Optional[str] = None
    time: Optional[str] = None
    catalyst: Optional[str] = None


class ReactionPrediction(BaseModel):
    reactants: str
    predicted_products: List[ReactionProduct]
    conditions: Optional[ReactionCondition] = None
    rationale: str


class RetroStep(BaseModel):
    step_index: int
    transformation: str
    product: Optional[str] = None
    precursors: List[str]
    reagents: Optional[str] = None
    conditions: Optional[str] = None


class RetroRoute(BaseModel):
    route_index: int
    steps: List[RetroStep]
    starting_materials: List[str]
    overall_rationale: str


class RetroPlan(BaseModel):
    target: str
    routes: List[RetroRoute]

