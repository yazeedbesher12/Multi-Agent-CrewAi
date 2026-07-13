from __future__ import annotations

import contextlib
import io
import os
import re
from pathlib import Path
from typing import Any

import streamlit as st
from dotenv import load_dotenv


APP_TITLE = "Research Crew"
CREW_FILE = Path(__file__).parent / "crew.jsonc"
REQUIRED_ENV_KEYS = ("OPENROUTER_API_KEY", "SERPER_API_KEY")
OPTIONAL_ENV_KEYS = ("MODEL", "APP_PASSWORD")


def read_secret(name: str) -> str | None:
    try:
        value = st.secrets.get(name)
    except Exception:
        return None

    if value is None:
        return None

    value = str(value).strip()
    return value or None


def configure_environment() -> list[str]:
    load_dotenv()

    for key in (*REQUIRED_ENV_KEYS, *OPTIONAL_ENV_KEYS):
        if not os.getenv(key):
            secret_value = read_secret(key)
            if secret_value:
                os.environ[key] = secret_value

    return [key for key in REQUIRED_ENV_KEYS if not os.getenv(key)]


def configured_password() -> str | None:
    value = os.getenv("APP_PASSWORD") or read_secret("APP_PASSWORD")
    if value is None:
        return None

    value = str(value)
    return value or None


def require_password() -> bool:
    password = configured_password()
    if not password or st.session_state.get("authenticated"):
        return True

    entered_password = st.text_input("Password", type="password")
    if st.button("Sign in", type="primary"):
        if entered_password == password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")

    return False


def redact_sensitive_text(text: str) -> str:
    redacted = text

    for key in (*REQUIRED_ENV_KEYS, *OPTIONAL_ENV_KEYS):
        value = os.getenv(key)
        if value:
            redacted = redacted.replace(value, "[redacted]")

    redacted = re.sub(
        r"(?i)(api[_-]?key|token|secret|password)(\s*[:=]\s*)([^\s,'\"]+)",
        r"\1\2[redacted]",
        redacted,
    )
    redacted = re.sub(r"sk-or-v1-[A-Za-z0-9_-]+", "[redacted-openrouter-key]", redacted)
    return redacted[:2000]


def friendly_error_message(error: Exception) -> str:
    detail = str(error).lower()

    if "429" in detail or "quota" in detail or "rate limit" in detail:
        return "OpenRouter quota or rate limit was reached. Try again later or check your balance."

    if "serper" in detail:
        return "There is a problem with Serper. Check your SERPER_API_KEY."

    if "openrouter" in detail:
        return "There is a problem with OpenRouter. Check OPENROUTER_API_KEY and the model name."

    return "An error occurred while running the research."


def extract_report(result: Any) -> str:
    raw = getattr(result, "raw", None)
    if isinstance(raw, str) and raw.strip():
        return raw
    if raw:
        return str(raw)
    return str(result)


def run_research(topic: str) -> str:
    from crewai.project import load_crew

    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        crew, default_inputs = load_crew(CREW_FILE)
        inputs = dict(default_inputs or {})
        inputs["topic"] = topic
        result = crew.kickoff(inputs=inputs)

    return extract_report(result)


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, layout="centered")
    st.markdown(
        """
        <style>
        .stApp, textarea {
            direction: ltr;
            text-align: left;
        }
        code, pre {
            direction: ltr;
            text-align: left;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    configure_environment()
    st.title("Research Interface")

    if not require_password():
        return

    missing_variables = configure_environment()
    if missing_variables:
        st.error("Add the following required environment variables:")
        st.code("\n".join(missing_variables), language="text")
        return

    if not CREW_FILE.exists():
        st.error("crew.jsonc was not found.")
        return

    st.session_state.setdefault("result", "")

    with st.form("research_form"):
        topic = st.text_area(
            "Enter the text or idea you want to research",
            height=170,
            placeholder="Example: I want to build an app that helps students summarize PDF files and create short quizzes.",
        )
        submitted = st.form_submit_button("Start Research", type="primary", use_container_width=True)

    if submitted:
        clean_topic = topic.strip()
        if not clean_topic:
            st.warning("Enter a research topic first.")
        else:
            try:
                with st.spinner("Researching and preparing the result..."):
                    st.session_state.result = run_research(clean_topic)
            except Exception as exc:
                st.session_state.result = ""
                st.error(friendly_error_message(exc))
                with st.expander("Error details"):
                    st.code(redact_sensitive_text(f"{type(exc).__name__}: {exc}"), language="text")

    st.divider()
    st.subheader("Result")
    if st.session_state.result:
        st.markdown(st.session_state.result)
    else:
        st.info("The research result will appear here after you start.")


if __name__ == "__main__":
    main()
