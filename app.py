# ---------------------------------------------------------------
"""
Build A Streamlit Interface For A Locally Installed LLM

Create a simple and interactive Streamlit web interface that connects to a locally
installed large language model (LLM) running via Ollama. The interface should
include a text input box for user queries and a response area to display
model-generated answers. Ensure smooth communication between the Streamlit
frontend and the LLM back-end using appropriate API calls or local endpoints.
Add basic features like a conversation history panel and a reset button to enhance
usability.
"""
#---------------------------------------------------------------

import streamlit as st
import requests
import json

# -------------------------------
# Streamlit page setup
# -------------------------------
st.set_page_config(page_title="ChatBot", page_icon="🤖", layout="centered")

# Visible title inside the page (this shows as a header in the app body)
st.title("Ollama ChatBot")

# -------------------------------
# Initialize chat history and defaults
# -------------------------------
if "history" not in st.session_state:
    st.session_state.history = []
if "model" not in st.session_state:
    # ✅ set your default installed model name (e.g., "llama3" or "phi3")
    st.session_state.model = "llama3"

OLLAMA_BASE = "http://localhost:11434"

# -------------------------------
# Check Ollama connection
# -------------------------------
def is_ollama_running(timeout=1.0):
    try:
        r = requests.get(f"{OLLAMA_BASE}/api/version", timeout=timeout)
        return r.ok
    except Exception:
        return False

# -------------------------------
# Query Ollama (with streaming)
# -------------------------------
def query_ollama(prompt, model="llama3", stream=True):
    url = f"{OLLAMA_BASE}/api/generate"
    payload = {"model": model, "prompt": prompt, "stream": stream}
    headers = {"Content-Type": "application/json"}

    try:
        resp = requests.post(url, json=payload, headers=headers, stream=stream, timeout=60)
    except Exception as e:
        return f"⚠️ Error connecting to Ollama: {e}"

    if not resp.ok:
        return f"⚠️ Ollama returned status {resp.status_code}: {resp.text}"

    if stream:
        full = ""
        container = st.empty()
        for line in resp.iter_lines(decode_unicode=True):
            if not line:
                continue
            try:
                data = json.loads(line)
                chunk = data.get("response") or data.get("text") or ""
            except Exception:
                chunk = line
            if chunk:
                full += chunk
                container.markdown(f"🤖 **LLM:** {full}")
        return full.strip()
    else:
        try:
            data = resp.json()
            return data.get("response") or data.get("text") or str(data)
        except Exception:
            return resp.text

# -------------------------------
# Get available models
# -------------------------------
def get_available_models(timeout=1.0):
    try:
        r = requests.get(f"{OLLAMA_BASE}/api/models", timeout=timeout)
        if not r.ok:
            return []
        data = r.json()
        if isinstance(data, list):
            return [m.get("name") if isinstance(m, dict) else str(m) for m in data]
        if isinstance(data, dict):
            candidates = data.get("models") or data.get("items") or []
            return [m.get("name") for m in candidates if isinstance(m, dict)]
    except Exception:
        return []

# -------------------------------
# Sidebar: Model selection & reset
# -------------------------------
st.sidebar.title("⚙️ Settings")
connected = is_ollama_running()
st.sidebar.write("Status:", "🟢 Running" if connected else "🔴 Not reachable")

available_models = get_available_models() if connected else []
# Offline fallback models (used if API listing fails) – make sure these are installed in Ollama
fallback = ["llama3", "phi3"]
options = available_models or fallback
if st.session_state.model not in options:
    st.session_state.model = options[0]

st.session_state.model = st.sidebar.selectbox("Select Model", options=options, index=options.index(st.session_state.model))

if st.sidebar.button("Reset Chat"):
    st.session_state.history = []
    st.success("Chat history cleared!")


# -------------------------------
# Show conversation history
# -------------------------------
chat_area = st.container()
with chat_area:
    # Iterate over history in pairs (user + bot)
    for i in range(0, len(st.session_state.history), 2):
        user_msg = st.session_state.history[i][1]
        st.markdown(f"🧑 **You:** {user_msg}")

        # Check if bot reply exists
        if i + 1 < len(st.session_state.history):
            bot_msg = st.session_state.history[i + 1][1]
            st.markdown(f"🤖 **LLM:** {bot_msg}")

        # Separator after full exchange
        st.write("--------------------------------------------------------------------------------------------------------------")


        



# -------------------------------
# User Input Form
# -------------------------------
with st.form("input_form", clear_on_submit=True):
    user_input = st.text_input("Enter your Query:")
    submitted = st.form_submit_button("Send")

    if submitted and user_input:
        # Append user message
        st.session_state.history.append(("user", user_input))
        
        # Query Ollama
        if not connected:
            bot_reply = "⚠️ Ollama not reachable at http://localhost:11434"
        else:
            with st.spinner("Thinking..."):
                bot_reply = query_ollama(user_input, model=st.session_state.model, stream=True)
        
        # Append bot response
        st.session_state.history.append(("bot", bot_reply))
        
  
      
        # Rerun to update chat area
        st.rerun()
