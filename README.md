# Research Crew

A simple Streamlit interface for the current CrewAI project. Enter a research topic or project idea, start the workflow, and view the generated result on the same page.

## Live App

https://multi-agent-crewai-g6szavwpmthv3b4wllhj2b.streamlit.app/

## Run Locally

```bash
uv sync
uv run streamlit run app.py
```

Then open the local URL printed by Streamlit, usually:

```text
http://localhost:8501
```

## Environment Variables

For local development, create a `.env` file in the project root:

```text
OPENROUTER_API_KEY="your-openrouter-key"
SERPER_API_KEY="your-serper-key"
```

For Streamlit Community Cloud, add the same values in:

`App settings` -> `Secrets`

```toml
OPENROUTER_API_KEY = "your-openrouter-key"
SERPER_API_KEY = "your-serper-key"
```

Do not commit real API keys to GitHub.

## Deploy On Streamlit Community Cloud

1. Open <https://share.streamlit.io>
2. Select the GitHub repository: `yazeedbesher12/Multi-Agent-CrewAi`
3. Select the branch: `master`
4. Set the app file to: `app.py`
5. Add the required secrets.
6. Deploy the app.

Public usage of the app consumes the configured OpenRouter and Serper quotas. To restrict access, add an optional password:

```toml
APP_PASSWORD = "your-password"
```
