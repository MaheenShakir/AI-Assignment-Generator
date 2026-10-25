import os
import time

import streamlit as st
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


# ---------- Look and feel (CSS) ----------
STYLE = """
<style>
.stApp {
    background: linear-gradient(160deg, #0b1020 0%, #131b35 100%);
    color: #e6e9f2;
}
header[data-testid="stHeader"] { background: transparent; }
footer { visibility: hidden; }
.block-container { max-width: 820px; padding-top: 2.5rem; }

.hero-title {
    font-size: 2.4rem; font-weight: 800; line-height: 1.2; margin: 0;
    background: linear-gradient(90deg, #6aa3ff, #a58bff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-sub { color: #9aa6c7; font-size: 1.05rem; margin: 0.4rem 0 1.5rem 0; }

/* cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(24, 33, 62, 0.75);
    border: 1px solid #2b3658;
    border-radius: 16px;
}

/* inputs */
.stTextInput label p { color: #b7c1de; font-weight: 600; }
.stTextInput input {
    background: #0f1630; color: #ffffff;
    border: 1px solid #2f3b66; border-radius: 10px;
}
.stTextInput input:focus { border-color: #6aa3ff; box-shadow: 0 0 0 1px #6aa3ff; }

/* button */
.stButton > button {
    width: 100%; border: none; border-radius: 10px;
    padding: 0.65rem 1.4rem; font-weight: 700; color: #ffffff;
    background: linear-gradient(90deg, #4f8bf9, #7a5af8);
}
.stButton > button:hover { opacity: 0.9; color: #ffffff; }

/* the generated assignment */
.stMarkdown p, .stMarkdown li { color: #dfe4f1; line-height: 1.75; }
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #ffffff; }
.stMarkdown table { border-collapse: collapse; width: 100%; }
.stMarkdown th, .stMarkdown td { border: 1px solid #34426f; padding: 8px 12px; }
.stMarkdown th { background: #1d2850; color: #ffffff; }
.stMarkdown code { color: #9fc2ff; }
h3, h2 { color: #ffffff; }
</style>
"""

# ---------- Page ----------
st.set_page_config(page_title="AI Assignment Generator", page_icon="📝", layout="centered")
st.markdown(STYLE, unsafe_allow_html=True)

st.markdown('<p class="hero-title">📝 AI Assignment Generator</p>', unsafe_allow_html=True)
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
    st.subheader("📋 Copy Assignment")
    st.caption("Click the copy icon at the top right of the box below.")
    st.code(st.session_state["assignment"], language=None, wrap_lines=True)
