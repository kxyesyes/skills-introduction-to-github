from typing import List, Dict, Any
from langchain.tools import tool
from duckduckgo_search import DDGS
import wikipedia
import arxiv
import os

from ..config import CONFIG


@tool("ddg_search", return_direct=False)
def ddg_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """Search DuckDuckGo and return a list of results with title, href, snippet."""
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=max_results))
    out = [
        {"title": r.get("title"), "href": r.get("href"), "snippet": r.get("body")}
        for r in results
    ]
    return out


@tool("wikipedia_search", return_direct=False)
def wikipedia_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """Search Wikipedia and return page titles and summaries."""
    wikipedia.set_lang("en")
    hits = wikipedia.search(query, results=max_results)
    results = []
    for title in hits:
        try:
            page = wikipedia.page(title, auto_suggest=False)
            results.append({"title": title, "url": page.url, "summary": wikipedia.summary(title, sentences=2)})
        except Exception:
            continue
    return results


@tool("arxiv_search", return_direct=False)
def arxiv_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """Search arXiv for papers; return title, url, summary."""
    search = arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance)
    results = []
    for r in search.results():
        results.append({"title": r.title, "url": r.entry_id, "summary": r.summary})
    return results


@tool("serpapi_search", return_direct=False)
def serpapi_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """Search using SerpAPI if configured; returns organic results with title, link, snippet."""
    key = CONFIG.serpapi_key or os.getenv("SERPAPI_API_KEY")
    if not key:
        return []
    import serpapi

    client = serpapi.Client(api_key=key)
    result = client.search({"engine": "google", "q": query, "num": max_results})
    organic = result.get("organic_results", [])
    out = [{"title": o.get("title"), "link": o.get("link"), "snippet": o.get("snippet")} for o in organic]
    return out


def make_ddg_search_tool():
    return ddg_search


def make_wikipedia_search_tool():
    return wikipedia_search


def make_arxiv_search_tool():
    return arxiv_search


def make_serpapi_search_tool():
    return serpapi_search

