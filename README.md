# 📝 AI Assignment Generator

A simple web app that writes a university-style assignment from a subject and a topic, using Python, Streamlit, and the Google Gemini API.

**Live demo:** https://ai-assignment-generator-lzi8yhumolbuwfujnukkze.streamlit.app/
   ![App screenshot](screenshot.png)
## How It Works
1. Enter a subject and an assignment topic.
2. Click **Generate Assignment**.
3. The app sends a prompt to Gemini and shows the result with headings and paragraphs.
4. Use the copy icon on the text box to copy the assignment.

## Tools Used
- Python
- Streamlit
- Google Gemini API (`google-genai`)

## Run Locally
1. Install the libraries: `pip install -r requirements.txt`
2. Get a free API key from https://aistudio.google.com/apikey
3. Set the key: `$env:GEMINI_API_KEY="your_key_here"` (Windows PowerShell)
4. Start the app: `streamlit run app.py`

The API key is never stored in the code. It is read from an environment variable or from Streamlit Secrets.
