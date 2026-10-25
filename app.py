import json
import os
import time

import streamlit as st
import streamlit.components.v1 as components
from google import genai

# Models are tried in order. If the first one is busy, the second is used.
MODELS = ["gemini-3.8-flash", "gemini-3.5-flash-lite"]


def get_api_key():
    """Get the API key from Streamlit secrets or an environment variable."""
    try:
        key = st.secrets["GEMINI_API_KEY"]
        if key:
            return key
    except Exception:
        pass  # no secrets file found, try the environment variable next
    return os.getenv("GEMINI_API_KEY")


def generate_assignment(topic, subject, api_key):
    """Ask Gemini to write the assignment and return the text."""
    client = genai.Client(api_key=api_key)

    prompt = f"""You are a BS student who writes clear, well-researched university assignments.
Write an assignment in your own natural voice.

Subject: {subject}
Topic: {topic}

Structure (use markdown headings, but write them like a real assignment, not a template):
- A clear title
- Introduction: a short paragraph that explains the topic and what the assignment covers
- 3 to 4 main sections with ### headings. Explain the ideas in connected paragraphs,
  give simple real-life examples, and add a short code example in a code block only
  if the topic is technical.
- One comparison table, only if the topic has two or more things worth comparing
- Real-world applications: a short paragraph or a few short points
- Conclusion: one short paragraph

Length: about 800 to 1000 words. Not too long and not too short.

Writing style rules:
- Write like a human student: plain, direct sentences of different lengths.
- Mostly paragraphs. Use bullet points rarely, and only where a list is natural.
- Do NOT use phrases like "delve", "in today's fast-paced world", "it is important to note",
  "plays a crucial role", "in the realm of", "game-changer", or "in conclusion".
- Do not use emojis. Avoid long dashes and avoid repeating the same sentence pattern.
- Do not add a "Key Takeaways" section.
- Do not invent references, quotes, or statistics.
"""

    last_error = None
    for model in MODELS:
        try:
            response = client.models.generate_content(model=model, contents=prompt)
            return response.text
        except Exception as error:
            last_error = error
            time.sleep(1)  # short pause, then try the next model
    raise last_error


# ---------- Choose your color theme here ----------
# Options: "graphite" (dark grey), "mono" (white and black), "fresh", "academic", "lavender", "slate"
THEME = "mono"

THEMES = {
    "graphite": {   # Dark grey + white
        "bg1": "#1b1c1f", "bg2": "#26282c", "card": "#2b2d32", "border": "#3e4148",
        "text": "#e9eaed", "muted": "#a5a9b2", "heading": "#ffffff",
        "input_bg": "#202226", "input_border": "#464a52",
        "a1": "#ffffff", "a2": "#cfd2d8", "btn_text": "#111214",
        "th_bg": "#373b42", "code": "#d6d9df", "shadow": "rgba(0,0,0,0.35)",
    },
    "mono": {   # White + black
        "bg1": "#ffffff", "bg2": "#eff0f2", "card": "#ffffff", "border": "#dcdee2",
        "text": "#2a2c31", "muted": "#6c7078", "heading": "#0f1012",
        "input_bg": "#f6f7f8", "input_border": "#cfd2d7",
        "a1": "#111214", "a2": "#3d4047", "btn_text": "#ffffff",
        "th_bg": "#eceef0", "code": "#111214", "shadow": "rgba(0,0,0,0.10)",
    },
    "fresh": {
        "bg1": "#f6f8fd", "bg2": "#e9eefb", "card": "#ffffff",
        "border": "#e0e6f3", "text": "#2b3245", "muted": "#66718d",
        "heading": "#141a33", "input_bg": "#f7f9fd", "input_border": "#d3daec",
        "a1": "#4f6ef7", "a2": "#7b5cf0", "btn_text": "#ffffff",
        "th_bg": "#eef2fb", "code": "#4f46e5", "shadow": "rgba(60,80,140,0.12)",
    },
    "academic": {
        "bg1": "#fbf8f2", "bg2": "#f2ecdf", "card": "#ffffff",
        "border": "#e7dfcd", "text": "#33302a", "muted": "#7a7466",
        "heading": "#1c1a16", "input_bg": "#fdfbf6", "input_border": "#dbd2be",
        "a1": "#14a395", "a2": "#0f766e", "btn_text": "#ffffff",
        "th_bg": "#f1ece0", "code": "#0f766e", "shadow": "rgba(90,70,30,0.12)",
    },
    "lavender": {
        "bg1": "#f9f6ff", "bg2": "#ece5fc", "card": "#ffffff",
        "border": "#e4dbf8", "text": "#332c4a", "muted": "#7a7096",
        "heading": "#1f1836", "input_bg": "#faf8ff", "input_border": "#d8cdf4",
        "a1": "#8b5cf6", "a2": "#ec6fb0", "btn_text": "#ffffff",
        "th_bg": "#f1ebfd", "code": "#7c3aed", "shadow": "rgba(100,70,170,0.12)",
    },
    "slate": {
        "bg1": "#233047", "bg2": "#2e3d58", "card": "#31405b",
        "border": "#46567a", "text": "#e7ecf5", "muted": "#aab7cd",
        "heading": "#ffffff", "input_bg": "#283650", "input_border": "#4d6082",
        "a1": "#2dd4bf", "a2": "#38bdf8", "btn_text": "#0b1a2b",
        "th_bg": "#3b4c6b", "code": "#7ee7da", "shadow": "rgba(0,0,0,0.25)",
    },
}


def build_style(name):
    """Turn the chosen color theme into CSS."""
    c = THEMES[name]
    variables = "".join(f"--{key}: {value};" for key, value in c.items())
    return "<style>:root {" + variables + "}" + """
.stApp { background: linear-gradient(160deg, var(--bg1) 0%, var(--bg2) 100%); color: var(--text); }
header[data-testid="stHeader"] { background: transparent; color: var(--text); }
header[data-testid="stHeader"] button, header[data-testid="stHeader"] svg { color: var(--text); fill: var(--text); }
footer { visibility: hidden; }
.block-container { max-width: 820px; padding-top: 2.5rem; }

h1.hero-title {
    font-size: 2.5rem !important; font-weight: 800 !important; line-height: 1.2 !important;
    margin: 0 !important; padding: 0 !important;
    background: linear-gradient(90deg, var(--a1), var(--a2));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
p.hero-sub { color: var(--muted) !important; font-size: 1.05rem; margin: 0.4rem 0 1.5rem 0; }

/* cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--card); border: 1px solid var(--border) !important;
    border-radius: 16px; box-shadow: 0 6px 18px var(--shadow);
}

/* inputs */
.stTextInput label p { color: var(--muted) !important; font-weight: 600; }
.stTextInput input {
    background: var(--input_bg); color: var(--text);
    border: 1px solid var(--input_border); border-radius: 10px;
}
.stTextInput input::placeholder { color: var(--muted); opacity: 0.7; }
.stTextInput input:focus { border-color: var(--a1); box-shadow: 0 0 0 1px var(--a1); }

/* button */
.stButton > button {
    width: 100%; border: none; border-radius: 10px;
    padding: 0.65rem 1.4rem; font-weight: 700; color: var(--btn_text);
    background: linear-gradient(90deg, var(--a1), var(--a2));
}
.stButton > button:hover { opacity: 0.92; color: var(--btn_text); }
.stButton > button p { color: var(--btn_text); }

/* text, assignment and tables */
.stMarkdown p, .stMarkdown li, .stMarkdown td { color: var(--text); line-height: 1.75; }
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, h2, h3 { color: var(--heading); }
.stMarkdown table { border-collapse: collapse; width: 100%; }
.stMarkdown th, .stMarkdown td { border: 1px solid var(--border); padding: 8px 12px; }
.stMarkdown th { background: var(--th_bg); color: var(--heading); }
.stMarkdown code { color: var(--code); }
[data-testid="stCaptionContainer"], .stSpinner p { color: var(--muted); }
</style>
"""


def copy_button(text, name):
    """Show a small Copy button that copies the whole assignment."""
    c = THEMES[name]
    safe_text = json.dumps(text).replace("</", "<\\/")
    html = """
    <meta charset="utf-8">
    <button id="copy-btn">📋 Copy Assignment</button>
    <style>
      body { margin: 0; }
      #copy-btn {
        border: none; border-radius: 10px; padding: 10px 18px; cursor: pointer;
        font-size: 15px; font-weight: 700; font-family: sans-serif;
        color: %(btn_text)s;
        background: linear-gradient(90deg, %(a1)s, %(a2)s);
      }
      #copy-btn:hover { opacity: 0.9; }
    </style>
    <script>
      const text = %(text)s;
      const button = document.getElementById("copy-btn");
      function fallbackCopy() {
        const box = document.createElement("textarea");
        box.value = text;
        document.body.appendChild(box);
        box.select();
        document.execCommand("copy");
        document.body.removeChild(box);
      }
      button.addEventListener("click", async () => {
        try {
          await navigator.clipboard.writeText(text);
        } catch (error) {
          fallbackCopy();
        }
        button.textContent = "✅ Copied!";
        setTimeout(() => { button.textContent = "📋 Copy Assignment"; }, 2000);
      });
    </script>
    """ % {"btn_text": c["btn_text"], "a1": c["a1"], "a2": c["a2"], "text": safe_text}
    components.html(html, height=60)


# ---------- Page ----------
st.set_page_config(page_title="AI Assignment Generator", page_icon="📝", layout="centered")
st.markdown(build_style(THEME), unsafe_allow_html=True)

st.markdown('<h1 class="hero-title">📝 AI Assignment Generator</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-sub">Enter a subject and a topic, and get a well-structured assignment in seconds.</p>',
    unsafe_allow_html=True,
)

with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        subject = st.text_input("Subject", placeholder="e.g. Data Structures")
    with col2:
        topic = st.text_input("Assignment topic", placeholder="e.g. Linked List vs Array")

    generate = st.button("✨ Generate Assignment")

if generate:
    # 1. Check the inputs
    if not subject.strip() or not topic.strip():
        st.error("Please enter both the subject and the topic.")
    else:
        # 2. Check the API key
        api_key = get_api_key()
        if not api_key:
            st.error("API key not found. Please set GEMINI_API_KEY (see the README).")
        else:
            # 3. Generate the assignment
            with st.spinner("Writing your assignment..."):
                try:
                    st.session_state["assignment"] = generate_assignment(
                        topic.strip(), subject.strip(), api_key
                    )
                except Exception as error:
                    st.error(f"Sorry, something went wrong: {error}")

# ---------- Show the result ----------
if "assignment" in st.session_state:
    st.write("")
    with st.container(border=True):
        st.markdown(st.session_state["assignment"])

    st.write("")
    copy_button(st.session_state["assignment"], THEME)

    with st.expander("Copy button not working? Show the plain text"):
        st.code(st.session_state["assignment"], language=None, wrap_lines=True)
