from __future__ import annotations

import contextlib
import io
import os
import re
from pathlib import Path
from typing import Any

import streamlit as st
from dotenv import load_dotenv


APP_TITLE = "AI Project Advisor"
CREW_FILE = Path(__file__).parent / "crew.jsonc"
SECRET_ENV_KEYS = ("MODEL", "OPENROUTER_API_KEY", "SERPER_API_KEY")
REQUIRED_ENV_KEYS = SECRET_ENV_KEYS


def _read_secret(name: str) -> str | None:
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

    for key in SECRET_ENV_KEYS:
        if not os.getenv(key):
            secret_value = _read_secret(key)
            if secret_value:
                os.environ[key] = secret_value

    return [key for key in REQUIRED_ENV_KEYS if not os.getenv(key)]


def configured_password() -> str | None:
    value = os.getenv("APP_PASSWORD") or _read_secret("APP_PASSWORD")
    if value is None:
        return None

    value = str(value)
    return value if value else None


def redact_sensitive_text(text: str) -> str:
    redacted = text

    for key in (*SECRET_ENV_KEYS, "APP_PASSWORD"):
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
        return (
            "تعذر إكمال التحليل بسبب حد الاستخدام أو الرصيد في OpenRouter. "
            "يرجى مراجعة الرصيد أو المحاولة لاحقا."
        )

    if "serper" in detail or "serper_api_key" in detail:
        return (
            "تعذر إجراء البحث على الويب عبر Serper. "
            "تحقق من مفتاح SERPER_API_KEY وحالة الخدمة."
        )

    if "openrouter" in detail or "openrouter_api_key" in detail:
        return (
            "تعذر الاتصال بنموذج OpenRouter. "
            "تحقق من OPENROUTER_API_KEY واسم النموذج."
        )

    return "حدث خطأ أثناء تشغيل الوكلاء. تحقق من التفاصيل التقنية المختصرة أدناه."


def extract_report(result: Any) -> str:
    raw = getattr(result, "raw", None)
    if isinstance(raw, str) and raw.strip():
        return raw

    if raw:
        return str(raw)

    return str(result)


def run_project_analysis(topic: str) -> str:
    from crewai.project import load_crew

    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        crew, default_inputs = load_crew(CREW_FILE)
        inputs = dict(default_inputs or {})
        inputs["topic"] = topic
        result = crew.kickoff(inputs=inputs)

    return extract_report(result)


def require_authentication(password: str | None) -> bool:
    if not password:
        return True

    if st.session_state.get("authenticated"):
        return True

    st.markdown("### تسجيل الدخول")
    entered_password = st.text_input("كلمة المرور", type="password")

    if st.button("دخول", type="primary"):
        if entered_password == password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("كلمة المرور غير صحيحة.")

    return False


def render_sidebar() -> None:
    with st.sidebar:
        st.header("سير العمل")
        st.markdown(
            """
            1. Technology Research Specialist
            2. Serper web research
            3. AI System Architect
            4. Final architecture report
            """
        )
        st.info("كل تشغيل يستهلك من رصيد OpenRouter وSerper.")


def render_app() -> None:
    st.title(APP_TITLE)
    st.caption(
        "واجهة عربية لتشغيل وكيلين من CrewAI: وكيل يبحث في فكرة المشروع، "
        "ثم وكيل معماري يحول النتائج إلى خطة تنفيذ وبنية تقنية واضحة."
    )

    missing_variables = configure_environment()
    if missing_variables:
        st.error("يلزم ضبط متغيرات البيئة التالية قبل تشغيل التحليل.")
        st.code("\n".join(missing_variables), language="text")
        return

    if not CREW_FILE.exists():
        st.error("تعذر العثور على ملف إعدادات الطاقم crew.jsonc.")
        return

    default_topic = st.session_state.get("topic", "")
    st.session_state.setdefault("report", "")
    st.session_state.setdefault("is_running", False)

    with st.form("project_advisor_form", clear_on_submit=False):
        topic = st.text_area(
            "فكرة المشروع",
            value=default_topic,
            height=170,
            placeholder=(
                "مثال: أريد بناء منصة عربية تساعد الطلاب على رفع ملفات PDF "
                "وتلخيصها، ثم إنشاء اختبارات قصيرة ومتابعة تقدم كل طالب."
            ),
            disabled=st.session_state.is_running,
        )
        submitted = st.form_submit_button(
            "تحليل المشروع",
            type="primary",
            disabled=st.session_state.is_running,
            use_container_width=True,
        )

    if submitted:
        clean_topic = topic.strip()

        if not clean_topic:
            st.warning("اكتب فكرة المشروع أولا.")
        elif len(clean_topic) < 15:
            st.warning("يرجى كتابة وصف أطول قليلا للفكرة، لا يقل عن 15 حرفا.")
        else:
            st.session_state.topic = clean_topic
            st.session_state.is_running = True

            try:
                with st.spinner("الوكلاء يعملون على البحث وبناء التقرير..."):
                    st.session_state.report = run_project_analysis(clean_topic)
            except Exception as exc:
                st.session_state.report = ""
                st.error(friendly_error_message(exc))
                with st.expander("تفاصيل تقنية مختصرة"):
                    st.code(redact_sensitive_text(f"{type(exc).__name__}: {exc}"), language="text")
            finally:
                st.session_state.is_running = False

    if st.session_state.report:
        st.divider()
        st.subheader("تقرير البنية وخطة التنفيذ")
        st.markdown(st.session_state.report)

        col_download, col_clear = st.columns([1, 1])
        with col_download:
            st.download_button(
                "تنزيل التقرير",
                data=st.session_state.report,
                file_name="architecture_report.md",
                mime="text/markdown",
                use_container_width=True,
            )
        with col_clear:
            if st.button("مسح التقرير الحالي", use_container_width=True):
                st.session_state.report = ""
                st.session_state.topic = ""
                st.rerun()


def main() -> None:
    st.set_page_config(
        page_title=APP_TITLE,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
        html, body, [class*="css"] {
            direction: rtl;
        }
        .stApp {
            text-align: right;
        }
        [data-testid="stSidebar"] {
            direction: rtl;
        }
        textarea {
            direction: rtl;
            text-align: right;
        }
        code, pre {
            direction: ltr;
            text-align: left;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    load_dotenv()
    if not require_authentication(configured_password()):
        return

    render_sidebar()
    render_app()


if __name__ == "__main__":
    main()
