from __future__ import annotations

import json
import os
from typing import Optional

import typer
from rich import print
from dotenv import load_dotenv

from .agent import build_agent
from .tools.properties import calculate_properties
from .tools.similarity import tanimoto_similarity, search_similar_in_dataset

app = typer.Typer(help="ChemAgent CLI")


def _ensure_env():
	load_dotenv(override=False)


@app.command()
def props(smiles: str):
	"""Calculate molecular properties for a SMILES string."""
	_ensure_env()
	print(calculate_properties(smiles))


@app.command()
def tanimoto(a: str, b: str):
	"""Compute Tanimoto similarity between two SMILES."""
	_ensure_env()
	print(tanimoto_similarity(a, b))


@app.command()
def simsearch(smiles: str, top_k: int = typer.Option(10, help="Top K results")):
	"""Search similar molecules in dataset."""
	_ensure_env()
	print(search_similar_in_dataset(smiles, top_k=top_k))


@app.command()
def chat(model: Optional[str] = typer.Option(None, help="Ollama model name")):
	"""Interactive chat with the ChemAgent."""
	_ensure_env()
	agent = build_agent(model_name=model)
	print("[bold green]ChemAgent ready. Type 'exit' to quit.[/bold green]")
	while True:
		try:
			q = input("> ").strip()
			if not q:
				continue
			if q.lower() in {"exit", "quit", ":q"}:
				break
			resp = agent.run(q)
			print(resp)
		except (KeyboardInterrupt, EOFError):
			break


if __name__ == "__main__":
	app()