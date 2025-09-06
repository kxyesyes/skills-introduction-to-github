# Introduction to GitHub

_Get started using GitHub in less than an hour._

## Welcome

People use GitHub to build some of the most advanced technologies in the world. Whether you’re visualizing data or building a new game, there’s a whole community and set of tools on GitHub that can help you do it even better. GitHub Skills’ “Introduction to GitHub” exercise guides you through everything you need to start contributing in less than an hour.

- **Who is this for**: New developers, new GitHub users, and students.
- **What you'll learn**: We'll introduce repositories, branches, commits, and pull requests.
- **What you'll build**: We'll make a short Markdown file you can use as your [profile README](https://docs.github.com/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme).
- **Prerequisites**: None. This exercise is a great introduction for your first day on GitHub.
- **How long**: This exercise takes less than one hour to complete.

In this exercise, you will:

1. Create a branch
2. Commit a file
3. Open a pull request
4. Merge your pull request

### How to start this exercise

1. Right-click **Copy Exercise** and open the link in a new tab.

   <a id="copy-exercise">
      <img src="https://img.shields.io/badge/📠_Copy_Exercise-AAA" height="25pt"/>
   </a>

2. In the new tab, most of the prompts will automatically fill in for you.
   - For owner, choose your personal account or an organization to host the repository.
   - We recommend creating a public repository, as private repositories will [use Actions minutes](https://docs.github.chttps://github.com/kxyesyes/skills-introduction-to-github/billing/managing-billing-for-github-actions/about-billing-for-github-actions).
   - Scroll down and click the **Create repository** button at the bottom of the form.

3. After your new repository is created, wait about 20 seconds for the exercise to be prepared and buttons updated. You will continue working from your copy of the exercise.
   - The **Copy Exercise** button will deactivate, changing to gray.
   - The **Start Exercise** button will activate, changing to green.
   - You will likely need to refresh the page.

4. Click **Start Exercise**. Follow the step-by-step instructions and feedback will be provided as you progress.

   <a id="start-exercise" href="https://github.com/kxyesyes/skills-introduction-to-github/issues/1">
      <img src="https://img.shields.io/badge/🚀_Start_Exercise-008000" height="25pt"/>
   </a>

> [!IMPORTANT]
> The **Start Exercise** button will activate after copying the repository. You will probably need to refresh the page.

---

&copy; 2025 GitHub &bull; [Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md) &bull; [MIT License](https://gh.io/mit)

## ChemAgent (LangChain + Ollama)

An extensible chemistry agent inspired by ChemCrow. It provides:

- Molecular property calculator: SMILES → MW, LogP, TPSA, HBD/HBA, etc.
- ADMET prediction: SMILES → absorption/distribution/metabolism/excretion/toxicity via pluggable backends.
- Reaction prediction: reactant SMILES → predicted products (API or LLM fallback).
- Retrosynthesis: product SMILES → suggested routes (API or LLM fallback).
- Similarity tools: Tanimoto between two molecules; search similar molecules in a local dataset.
- Literature/knowledge search: DuckDuckGo, Wikipedia, arXiv, SerpAPI (optional).

Backed by LangChain and a local Ollama model (e.g., `llama3`).

### Setup

1) System prerequisites
- Install Ollama and pull a model (e.g., `ollama pull llama3`).
- Python 3.10+ recommended.

2) Create environment and install deps
```bash
cd /workspace
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

3) Configure environment
- Copy `.env.example` to `.env` and fill in any API keys or endpoints you have.
- For similarity search, place a dataset at `chemagent/data/molecules.csv` or `chemagent/data/molecules.smi` (see format below).

### RDKit
- RDKit is optional by default to ease installation. To enable property and similarity tools, install RDKit.
- Recommended: use a Python version and platform with prebuilt wheels. Example:
```bash
pip install rdkit-pypi==2022.9.5
```
If wheels are unavailable, use Conda: `conda install -c rdkit rdkit`.

### SerpAPI
- To enable `serpapi_search`, set `SERPAPI_API_KEY` in `.env`.

### Dataset formats
- `chemagent/data/molecules.csv` with columns: `smiles,name` (name optional)
- or `chemagent/data/molecules.smi`, whitespace-separated: `SMILES  Name` per line (name optional)

### Run the CLI
```bash
source .venv/bin/activate
python -m chemagent.cli chat --model llama3
```
Example commands inside the chat:
- "计算这个分子的性质: C1=CC=CC=C1O"
- "预测ADMET: CC(=O)Oc1ccccc1C(=O)O"
- "两个分子相似度: c1ccccc1, C1=CC=CC=C1O"
- "对这个反应物预测产物: CCBr.O=C=O"

You can also call tools directly:
```bash
python -m chemagent.cli props "C1=CC=CC=C1O"
python -m chemagent.cli tanimoto "c1ccccc1" "C1=CC=CC=C1O"
python -m chemagent.cli simsearch "CCO" --top-k 5
```

### Optional external backends
- ADMET: set `ADMET_API_URL` to a service that accepts `POST {"smiles": "..."}` and returns JSON fields for ADMET endpoints.
- Reaction prediction: set `REACTION_API_URL` similarly, or rely on LLM fallback.
- Retrosynthesis: set `RETRO_API_URL`, or rely on LLM fallback.
- SerpAPI: set `SERPAPI_API_KEY` to enable SerpAPI-powered search.

### Notes
- RDKit is required for most chemistry tools. If import fails, the tool will report a helpful error.
- LLM fallbacks are heuristic and for research only; do not use for critical decisions.