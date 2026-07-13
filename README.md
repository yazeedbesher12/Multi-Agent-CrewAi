# AI Project Advisor

A JSON-first CrewAI project with a Streamlit interface for turning a project
idea into a researched architecture and implementation plan.

The app reuses `crew.jsonc`, `agents/*.jsonc`, the existing task chain,
OpenRouter, and Serper. It creates a fresh crew for every submitted topic and
does not duplicate agent or task definitions in Python.

## Local Setup

```bash
uv sync
uv run streamlit run app.py
```

Open the local URL printed by Streamlit, enter a project idea, and submit the
form. Each run uses OpenRouter and Serper quota.

## Environment Variables

Create a local `.env` file with:

```text
MODEL="openrouter/openrouter/free"
OPENROUTER_API_KEY="your-openrouter-key"
SERPER_API_KEY="your-serper-key"
APP_PASSWORD="optional-local-password"
```

`APP_PASSWORD` is optional. When it is configured, the app asks for it before
showing the main interface. Do not commit real secrets.

## Streamlit Community Cloud

Deploy from <https://share.streamlit.io>:

1. Select the GitHub repository:
   `yazeedbesher12/Multi-Agent-CrewAi`.
2. Use the current branch: `master`.
3. Set the app entrypoint to `app.py`.
4. Set Python to `3.13`.
5. In Advanced settings, add top-level secrets:

```toml
MODEL = "openrouter/openrouter/free"
OPENROUTER_API_KEY = "replace-with-real-value"
SERPER_API_KEY = "replace-with-real-value"
APP_PASSWORD = "optional-password"
```

6. Choose public or private sharing based on who should access the app.
7. Deploy and inspect the build logs if the first build fails.

Every public use can consume OpenRouter and Serper quota. Configure
`APP_PASSWORD` if the app should not be open to anyone with the URL.

## Project Structure

- `app.py` - Streamlit UI for the CrewAI workflow
- `agents/` - Agent definitions (JSONC)
- `crew.jsonc` - Crew definition with tasks and configuration
- `tools/` - Custom tools (Python)
- `knowledge/` - Knowledge files for agents
- `.streamlit/config.toml` - Streamlit theme
- `.streamlit/secrets.toml.example` - Placeholder-only secrets template

> **Note:** `custom:<name>` tool references execute `tools/<name>.py` as local
> Python code when the crew loads. Only run crew projects from sources you
> trust.
