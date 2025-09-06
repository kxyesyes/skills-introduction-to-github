from __future__ import annotations

import json
import os
from typing import List

from duckduckgo_search import DDGS
import wikipedia
import arxiv

try:
	from serpapi import GoogleSearch  # type: ignore
	_HAS_SERP = True
except Exception:  # pragma: no cover
	_HAS_SERP = False


def web_search_tool(query: str) -> str:
	results: List[dict] = []
	with DDGS() as ddgs:
		for r in ddgs.text(query, max_results=8):
			results.append({
				"title": r.get("title"),
				"snippet": r.get("body"),
				"link": r.get("href"),
			})
	return json.dumps(results, ensure_ascii=False)


def serpapi_search_tool(query: str) -> str:
	api_key = os.getenv("SERPAPI_API_KEY")
	if not api_key or not _HAS_SERP:
		return json.dumps({
			"error": "SERPAPI_API_KEY not set or serpapi package unavailable."
		}, ensure_ascii=False)
	params = {
		"engine": "google",
		"q": query,
		"api_key": api_key,
		"num": 10,
	}
	search = GoogleSearch(params)
	resp = search.get_dict()
	items = []
	for item in resp.get("organic_results", [])[:10]:
		items.append({
			"title": item.get("title"),
			"snippet": item.get("snippet"),
			"link": item.get("link"),
		})
	return json.dumps(items, ensure_ascii=False)


def wikipedia_summary_tool(query: str) -> str:
	try:
		page = wikipedia.page(query, auto_suggest=True)
		return json.dumps({
			"title": page.title,
			"summary": wikipedia.summary(query, sentences=3, auto_suggest=True),
			"url": page.url,
		}, ensure_ascii=False)
	except Exception as e:
		return json.dumps({"error": str(e)}, ensure_ascii=False)


def arxiv_search_tool(query: str) -> str:
	client = arxiv.Client(page_size=5)
	search = arxiv.Search(query=query, max_results=5, sort_by=arxiv.SortCriterion.SubmittedDate)
	entries: List[dict] = []
	for r in client.results(search):
		entries.append({
			"title": r.title,
			"summary": r.summary[:400],
			"published": r.published.isoformat() if r.published else None,
			"pdf_url": r.pdf_url,
		})
	return json.dumps(entries, ensure_ascii=False)