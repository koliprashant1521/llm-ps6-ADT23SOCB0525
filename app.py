import os
import json
import html
import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

# Tried in order; the first model that responds is used.
MODELS = [
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
    "qwen/qwen3.8-27b",
]

SYSTEM = """You are a professional email assistant.
Given an email, write exactly three reply drafts:
1. formal   - polite, professional, complete sentences
2. friendly - warm, conversational, still respectful
3. short    - 2-3 sentences maximum
Rules: answer every question in the email, do not invent facts, dates or
commitments, and leave placeholders like [your name] where info is missing.
If the sender's name is known, address them by name. If the user's name is
given, use it in the sign-off.
Return ONLY JSON: {"formal": "...", "friendly": "...", "short": "..."}"""

SAMPLES = {
    "Meeting request": "Subject: Meeting on project timeline\n\nHi,\n\nCan we schedule a meeting on Friday to discuss the project timeline? Please let me know what time works for you.\n\nRegards,\nAnil",
    "Delivery complaint": "Subject: Order not delivered - urgent\n\nDear Support Team,\n\nI ordered a laptop bag 10 days ago (Order No. 48213), but it has still not arrived. The tracking page shows no update since last week. Please resolve this urgently or issue a refund.\n\nThank you,\nSneha",
    "Leave request": "Subject: Leave application for 25-27 November\n\nHello Sir,\n\nI would like to request leave from 25 to 27 November due to a family function. I will complete my pending work before leaving. Please let me know if this is approved.\n\nThanks,\nRahul",
    "Internship offer": "Subject: Internship Offer - Data Analyst Intern\n\nDear Candidate,\n\nWe are pleased to offer you a 3-month internship starting 1 December. Please confirm your acceptance by Monday.\n\nBest regards,\nHR Team",
    "Vague follow-up": "Subject: Re: Earlier message\n\nHey,\n\nDid you see what I sent earlier? Let me know your thoughts when you get a chance.\n\nCheers,\nPriya",
}

TABS = [("formal", "Formal"), ("friendly", "Friendly"), ("short", "Short")]


def call_llm(email_text, extra="", my_name=""):
    client = Groq(api_key=API_KEY)
    user = (
        f"Email:\n{email_text}\n\n"
        f"User's name: {my_name or 'not given'}\n"
        f"Extra instructions: {extra or 'none'}"
    )
    last_error = None
    for model in MODELS:
        try:
            r = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": user},
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
            )
            st.session_state["model_used"] = model
            return json.loads(r.choices[0].message.content)
        except Exception as e:
            last_error = e
    raise last_error


def copy_button(text):
    safe = json.dumps(text).replace("</", "<\\/")
    components.html(
        f"""
        <button id="b" onclick="c()" style="font:600 14px 'Inter',system-ui,sans-serif;
          background:#fff;color:#1D4E89;border:1px solid #1D4E89;border-radius:8px;
          padding:8px 16px;cursor:pointer">Copy reply</button>
        <script>
        function c() {{
          const t = {safe};
          const b = document.getElementById('b');
          const done = () => {{ b.innerText = 'Copied'; setTimeout(() => b.innerText = 'Copy reply', 1500); }};
          function fb() {{
            const a = document.createElement('textarea');
            a.value = t; document.body.appendChild(a); a.select();
            document.execCommand('copy'); document.body.removeChild(a); done();
          }}
          if (navigator.clipboard && window.isSecureContext) {{
            navigator.clipboard.writeText(t).then(done).catch(fb);
          }} else {{ fb(); }}
        }}
        </script>
        """,
        height=46,
    )


def load_sample():
    choice = st.session_state.get("sample", "None")
    if choice in SAMPLES:
        st.session_state["email_text"] = SAMPLES[choice]
        st.session_state.pop("out", None)


def clear_all():
    st.session_state["email_text"] = ""
    st.session_state["extra"] = ""
    st.session_state["sample"] = "None"
    st.session_state.pop("out", None)


# ---------- Page setup ----------
st.set_page_config(page_title="Email Reply Assistant", page_icon="✉️", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"], .stApp { font-family: 'Inter', system-ui, sans-serif; }
    #MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
    .block-container { padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1180px; }
    h1.app-title { font-size: 1.9rem; font-weight: 700; margin: 0; color: #1B2430; letter-spacing: -0.01em; }
    p.app-sub { color: #5B6675; margin: 0.25rem 0 1.6rem 0; font-size: 1rem; }
    .panel-title { font-weight: 600; font-size: 1.05rem; color: #1B2430; margin-bottom: 0.4rem; }
    .reply-card { background: #FFFFFF; border: 1px solid #E1E5EB; border-radius: 10px;
        padding: 1.3rem 1.5rem; line-height: 1.7; color: #1B2430; font-size: 0.98rem; }
    .meta { color: #5B6675; font-size: 0.85rem; margin: 0.6rem 0 0.2rem 0; }
    .empty { border: 1px dashed #C9D0DA; border-radius: 10px; padding: 2.4rem 1.5rem;
        color: #5B6675; text-align: center; background: #FFFFFF; }
    .stTextArea textarea, .stTextInput input { border-radius: 8px; }
    button[kind="primary"], [data-testid="stBaseButton-primary"] { border-radius: 8px; font-weight: 600; }
    .stTabs [data-baseweb="tab"] { font-weight: 600; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<h1 class="app-title">Email Reply Assistant</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="app-sub">Paste an email and get three ready-to-send replies: formal, friendly and short.</p>',
    unsafe_allow_html=True,
)

if not API_KEY:
    st.error("GROQ_API_KEY is missing. Copy .env.example to .env and add your key.")
    st.stop()

left, right = st.columns([5, 6], gap="large")

# ---------- Left: input ----------
with left:
    st.markdown('<div class="panel-title">Incoming email</div>', unsafe_allow_html=True)
    st.selectbox(
        "Load a sample email",
        ["None"] + list(SAMPLES.keys()),
        key="sample",
        on_change=load_sample,
    )
    email = st.text_area(
        "Email text",
        key="email_text",
        height=250,
        placeholder="Paste the email you received here...",
        label_visibility="collapsed",
    )
    my_name = st.text_input("Your name (used in the sign-off)", key="my_name", placeholder="e.g. Prashant")
    extra = st.text_input(
        "What should the reply say? (optional)",
        key="extra",
        placeholder="e.g. I am free on Friday after 3 PM",
    )
    b1, b2 = st.columns([3, 1])
    generate = b1.button("Generate replies", type="primary", use_container_width=True)
    b2.button("Clear", on_click=clear_all, use_container_width=True)

    if generate:
        if not email.strip():
            st.warning("Paste an email first.")
        else:
            with st.spinner("Writing your replies..."):
                try:
                    st.session_state["out"] = call_llm(email, extra, my_name)
                except Exception as e:
                    st.error(f"Could not generate replies. {e}")

# ---------- Right: output ----------
with right:
    st.markdown('<div class="panel-title">Suggested replies</div>', unsafe_allow_html=True)
    out = st.session_state.get("out")
    if not out:
        st.markdown(
            '<div class="empty">Your replies will appear here.<br>'
            "Paste an email on the left, or load a sample, then select Generate replies.</div>",
            unsafe_allow_html=True,
        )
    else:
        tabs = st.tabs([label for _, label in TABS])
        for tab, (key, label) in zip(tabs, TABS):
            with tab:
                text = str(out.get(key, "")).strip()
                card = html.escape(text).replace("\n", "<br>")
                st.markdown(f'<div class="reply-card">{card}</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="meta">{len(text.split())} words</div>',
                    unsafe_allow_html=True,
                )
                copy_button(text)

        all_text = "\n\n".join(
            f"=== {label.upper()} ===\n{str(out.get(key, '')).strip()}" for key, label in TABS
        )
        st.download_button("Download all replies (.txt)", all_text, file_name="email_replies.txt")
        if "model_used" in st.session_state:
            st.caption(f"Generated with {st.session_state['model_used']}")
