# Research Crew

واجهة Streamlit بسيطة لتشغيل مشروع CrewAI الحالي: تكتب فكرة أو نص البحث، تضغط زر البدء، ثم تظهر النتيجة في نفس الصفحة.

## التشغيل المحلي

```bash
uv sync
uv run streamlit run app.py
```

بعد التشغيل افتح الرابط المحلي الذي يظهر في الطرفية، غالبًا:

```text
http://localhost:8501
```

## متغيرات التشغيل

محليًا، ضع المفاتيح في ملف `.env`:

```text
OPENROUTER_API_KEY="your-openrouter-key"
SERPER_API_KEY="your-serper-key"
APP_PASSWORD="optional-password"
```

على Streamlit Community Cloud، أضف نفس القيم من صفحة Secrets. لا ترفع المفاتيح الحقيقية إلى GitHub.

## النشر على Streamlit

1. ادخل إلى Streamlit Community Cloud: <https://share.streamlit.io>
2. اختر المستودع: `yazeedbesher12/Multi-Agent-CrewAi`
3. اختر الفرع: `master`
4. اجعل ملف التطبيق: `app.py`
5. أضف Secrets:

```toml
OPENROUTER_API_KEY = "replace-with-real-value"
SERPER_API_KEY = "replace-with-real-value"
APP_PASSWORD = "optional-password"
```

6. اضغط Deploy.

بعد النشر سيظهر رابط بالشكل:

```text
https://your-app-name.streamlit.app
```

يمكن تغيير اسم الرابط من إعدادات التطبيق في Streamlit Cloud.
