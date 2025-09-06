import os
from typing import List

from langchain.agents import AgentType, initialize_agent, Tool
from langchain_ollama import ChatOllama
from langchain_core.language_models.chat_models import BaseChatModel

from .tools.properties import calculate_properties
from .tools.similarity import tanimoto_similarity, search_similar_in_dataset
from .tools.search import web_search_tool, wikipedia_summary_tool, arxiv_search_tool, serpapi_search_tool
from .tools.admet import predict_admet
from .tools.reactions import predict_reaction_products
from .tools.retrosyn import retrosynthesis_routes


def _build_model(model_name: str | None = None, temperature: float | None = None) -> BaseChatModel:
	name = model_name or os.getenv("MODEL_NAME", "llama3")
	temp = float(temperature if temperature is not None else os.getenv("MODEL_TEMPERATURE", 0.1))
	return ChatOllama(model=name, temperature=temp)


def build_tools() -> List[Tool]:
	tools: List[Tool] = []

	tools.append(
		Tool(
			name="molecular_properties",
			description=(
				"计算分子基本性质。输入SMILES，输出分子量、LogP、TPSA、HBD/HBA、可旋转键等。"
			),
			func=lambda q: calculate_properties(q),
		)
	)

	tools.append(
		Tool(
			name="tanimoto_similarity",
			description=(
				"计算两个分子的Tanimoto相似度。输入格式：SMILES1 || SMILES2"
			),
			func=lambda q: tanimoto_similarity(*[s.strip() for s in q.split("||", 1)]),
		)
	)

	tools.append(
		Tool(
			name="similarity_search_dataset",
			description=(
				"在本地数据集中搜索与输入分子最相似的分子。输入SMILES；使用CHEMAGENT_DATA下的molecules.csv或molecules.smi"
			),
			func=lambda q: search_similar_in_dataset(q),
		)
	)

	tools.append(
		Tool(
			name="admet_predict",
			description=(
				"预测分子ADMET性质。优先调用ADMET_API_URL；无则返回基于性质的启发式估计。"
			),
			func=lambda q: predict_admet(q),
		)
	)

	tools.append(
		Tool(
			name="reaction_predict",
			description=(
				"反应预测：输入反应物SMILES（用 . 分隔多组），输出可能产物。优先调用REACTION_API_URL，否则LLM启发式。"
			),
			func=lambda q: predict_reaction_products(q),
		)
	)

	tools.append(
		Tool(
			name="retrosynthesis",
			description=(
				"逆合成分析：输入目标产物SMILES，返回可能的合成路线。优先调用RETRO_API_URL，否则LLM启发式。"
			),
			func=lambda q: retrosynthesis_routes(q),
		)
	)

	# Web / literature search tools
	tools.append(
		Tool(
			name="web_search",
			description="DuckDuckGo网络检索，返回标题、摘要、链接。输入自然语言查询。",
			func=lambda q: web_search_tool(q),
		)
	)

	tools.append(
		Tool(
			name="wikipedia_summary",
			description="Wikipedia词条摘要检索。输入查询词。",
			func=lambda q: wikipedia_summary_tool(q),
		)
	)

	tools.append(
		Tool(
			name="arxiv_search",
			description="arXiv论文检索，返回若干最新相关条目。输入自然语言查询。",
			func=lambda q: arxiv_search_tool(q),
		)
	)

	tools.append(
		Tool(
			name="serpapi_search",
			description="SerpAPI谷歌搜索（需要SERPAPI_API_KEY）。",
			func=lambda q: serpapi_search_tool(q),
		)
	)

	return tools


def build_agent(model_name: str | None = None, temperature: float | None = None):
	llm = _build_model(model_name, temperature)
	tools = build_tools()
	agent = initialize_agent(
		tools=tools,
		llm=llm,
		agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
		verbose=False,
	)
	return agent