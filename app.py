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

    prompt = f"""Write a university-level assignment for a BS student.

Subject: {subject}
Topic: {topic}

Use this structure, with markdown headings:
# Title
## Introduction
## Main Content (use 3 to 4 sub-headings with short paragraphs)
## Conclusion

Rules:
- Use simple, clear English.
- Write about 600 to 800 words.
- Use proper paragraphs, not just bullet points.
- Do not invent references or quotes.
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


# ---------- Page ----------
st.set_page_config(page_title="AI Assignment Generator", page_icon="📝")

st.title("📝 AI Assignment Generator")
st.write("Enter a subject and a topic, and the AI will write an assignment for you.")

subject = st.text_input("Subject", placeholder="e.g. Data Science")
topic = st.text_input("Assignment topic", placeholder="e.g. Overfitting in Machine Learning")

if st.button("Generate Assignment", type="primary"):
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
    st.markdown("---")
    st.markdown(st.session_state["assignment"])

    st.markdown("---")
    st.subheader("Copy Assignment")
    st.caption("Click the copy icon at the top right of the box below.")
    st.code(st.session_state["assignment"], language=None, wrap_lines=True)
