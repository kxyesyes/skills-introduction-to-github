## Pharm Agent (Chemcrow-inspired)

Pharmaceutical chemistry assistants built with LangChain, RDKit, and local/remote LLMs (Ollama or Qwen-compatible OpenAI API).

### Features
- RDKit molecular properties (MW, LogP, TPSA, HBD/HBA, formula)
- ADMET prediction (heuristics + external API hook)
- Reaction prediction (API or LLM heuristic)
- Retrosynthesis analysis (LLM heuristic)
- Similarity search (Tanimoto) on a local dataset
- Literature search (DuckDuckGo, Wikipedia, arXiv, SerpAPI)
- Visualization (molecule image, property plots)

### Install
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Optional: install package for easy module execution
pip install -e .
```

RDKit wheels are used via `rdkit-pypi`. If you have system RDKit, adjust as needed.

### LLM Configuration
- Ollama (local): set `PROVIDER=ollama`, ensure `ollama` is running. Optionally set `OLLAMA_MODEL=llama3`.
- Qwen/OpenAI-compatible: set `PROVIDER=openai`, `OPENAI_API_KEY=...`, optionally `OPENAI_API_BASE` and `OPENAI_MODEL` (e.g., `qwen2.5` on a compatible endpoint that speaks OpenAI API).

Environment variables:
```
PROVIDER=ollama|openai
OLLAMA_MODEL=llama3
OPENAI_API_KEY=sk-...
OPENAI_API_BASE=https://api.your-endpoint
OPENAI_MODEL=gpt-4o-mini or qwen2.5

# System role
SYSTEM_PROMPT=You are PharmAgent, a senior pharmaceutical chemistry expert.

# Optional external services
ADMET_API_URL=https://...
REACTION_API_URL=https://...
RETRO_API_URL=https://...
SERPAPI_API_KEY=...
```

### Dataset
Place a CSV at `dataset/sample_mols.csv` with a `smiles` column and optional metadata. A small placeholder is included.

### CLI Usage
```bash
# if installed with -e .
pharm-agent props "CCO"
pharm-agent admet "CCO"
pharm-agent reaction "CCO" "+ O=O"
pharm-agent retro "CC(=O)OC1=CC=CC=C1C(=O)O"
pharm-agent similar "CCO" --top-k 5
pharm-agent search --query "ACE inhibitors binding" --engine ddg
pharm-agent draw "CCO" --out ethanol.png
pharm-agent agent

# or via module
python -m pharm_agent.cli props "CCO"
python -m pharm_agent.cli admet "CCO"
python -m pharm_agent.cli reaction "CCO" "+ O=O"
python -m pharm_agent.cli retro "CC(=O)OC1=CC=CC=C1C(=O)O"
python -m pharm_agent.cli similar "CCO" --top-k 5
python -m pharm_agent.cli search --query "ACE inhibitors binding" --engine ddg
python -m pharm_agent.cli draw "CCO" --out ethanol.png
python -m pharm_agent.cli agent
```

### Reference
Inspired by ChemCrow: `https://github.com/ur-whitelab/chemcrow-public.git`.

### Structured Output Format

Reaction prediction (`reaction_predict`) returns JSON:
```
{
  "reactants": "CCO + O=O",
  "predicted_products": [
    {"smiles": "CC=O", "name": "acetaldehyde", "confidence": 0.62}
  ],
  "conditions": {"reagents": "PCC", "solvent": "DCM", "temperature": "rt"},
  "rationale": "..."
}
```

Retrosynthesis (`retrosynthesis`) returns JSON:
```
{
  "target": "CC(=O)OC1=CC=CC=C1C(=O)O",
  "routes": [
    {
      "route_index": 1,
      "steps": [
        {"step_index": 1, "transformation": "esterification", "product": "aspirin", "precursors": ["salicylic acid", "acetic anhydride"], "reagents": "H2SO4", "conditions": "reflux"}
      ],
      "starting_materials": ["salicylic acid", "acetic anhydride"],
      "overall_rationale": "..."
    }
  ]
}
```

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