import json
from typing import Optional
import typer
from rich import print

from .tools import (
    make_props_tool,
    make_admet_tool,
    make_reaction_tool,
    make_retro_tool,
    SimilarityIndex,
    make_similarity_tool,
    make_ddg_search_tool,
    make_wikipedia_search_tool,
    make_arxiv_search_tool,
    make_serpapi_search_tool,
    make_draw_tool,
)
from .agent import build_agent


app = typer.Typer(help="Pharm Agent CLI")


@app.command()
def props(smiles: str):
    tool = make_props_tool()
    res = tool.run(smiles)
    print(res)


@app.command()
def admet(smiles: str):
    tool = make_admet_tool()
    res = tool.run(smiles)
    print(res)


@app.command()
def reaction(reactants: str):
    tool = make_reaction_tool()
    res = tool.run(reactants)
    print(res)


@app.command()
def retro(target: str):
    tool = make_retro_tool()
    res = tool.run(target)
    print(res)


@app.command()
def similar(smiles: str, top_k: int = typer.Option(5, help="Top K similar molecules")):
    tool = make_similarity_tool()
    res = tool.run(smiles, top_k=top_k)
    print(res)


@app.command()
def search(query: str, engine: str = typer.Option("ddg", help="ddg|wiki|arxiv|serp")):
    if engine == "ddg":
        tool = make_ddg_search_tool()
    elif engine == "wiki":
        tool = make_wikipedia_search_tool()
    elif engine == "arxiv":
        tool = make_arxiv_search_tool()
    elif engine == "serp":
        tool = make_serpapi_search_tool()
    else:
        raise typer.BadParameter("Unknown engine")
    res = tool.run(query)
    print(json.dumps(res, indent=2))


@app.command()
def draw(smiles: str, out: str = typer.Option("molecule.png"), size: int = typer.Option(300)):
    tool = make_draw_tool()
    res = tool.run(smiles, out, size)
    print(res)


@app.command()
def agent():
    tools = [
        make_props_tool(),
        make_admet_tool(),
        make_reaction_tool(),
        make_retro_tool(),
        make_similarity_tool(),
        make_ddg_search_tool(),
        make_wikipedia_search_tool(),
        make_arxiv_search_tool(),
        make_serpapi_search_tool(),
        make_draw_tool(),
    ]
    ag = build_agent(tools)
    print("Type your query. Ctrl+C to exit.")
    try:
        while True:
            q = input("pharm> ")
            if not q:
                continue
            ans = ag.run(q)
            print(ans)
    except KeyboardInterrupt:
        print("\nBye.")


def main():
    app()


if __name__ == "__main__":
    main()

