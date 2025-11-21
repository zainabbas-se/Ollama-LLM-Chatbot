## 🤖 Ollama LLM Chatbot

A simple, production-ready **Streamlit interface** for chatting with a locally installed **Large Language Model (LLM)** using **Ollama**.  
It provides an easy-to-use web interface where users can type queries, view responses, and maintain chat history — all running locally and privately.

---

## 🚀 Features

- **🧠 Local Ollama LLM** – Connects directly to a locally hosted Ollama LLM (e.g. `llama3`, `phi3`).
- **💬 Interactive Chat UI** – Clean chat interface built with Streamlit.
- **🕒 Conversation History** – Previous messages displayed in an organized layout.
- **🔄 Reset Chat** – Button to clear previous chats and start fresh.
- **⚙️ Model Selection** – Choose from available Ollama models.
- **✅ Connection Check** – Verifies connectivity to the Ollama server automatically.

---

## 🧩 Requirements

- **Python** 3.9+
- **Ollama** (installed and running locally)
- **Python libraries**: `streamlit`, `requests` (installed via `requirements.txt`)

---

## 📦 Installation & Setup

> All commands below use **bash** syntax. On Windows with PowerShell, just adjust path/activation accordingly.

### 1️⃣ Clone the Repository

```bash
git clone <YOUR_REPO_URL> "Ollama LLM Chatbot"
cd "Ollama LLM Chatbot"
```

### 2️⃣ Create and Activate a Virtual Environment

```bash
# Create venv
python -m venv .venv

# Activate venv (Linux / macOS)
source .venv/bin/activate

# Activate venv (Windows Git Bash)
source .venv/Scripts/activate
```

> On Windows PowerShell, you’d instead run:  
> `.\.venv\Scripts\Activate.ps1`

### 3️⃣ Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4️⃣ Install and Run Ollama

1. Download and install Ollama from the official site (`https://ollama.com`).
2. Pull your preferred model (example: `llama3.1`):

```bash
ollama pull llama3.1
```

3. Ensure the Ollama daemon is running in the background.

### 5️⃣ Configure Environment (Optional)

If your project uses environment variables (e.g. for data paths or model names), create a `.env` file:

```bash
cp .env.example .env
# then edit .env with your own settings
```

(If there is no `.env.example`, you can skip this step or create `.env` based on your own needs.)

### 6️⃣ Run the App

```bash
streamlit run app.py
```

Then open the URL shown in your terminal (usually `http://localhost:8501`) in your browser.

---

## 💡 How It Works

- **Ingestion & Indexing**
  - Your documents are loaded and split into chunks.
  - Each chunk is converted into an **embedding vector** and stored in a lightweight vector index.

- **Query Processing**
  - When you ask a question, it’s embedded and used to search the index.
  - The most relevant chunks are retrieved as **context** for the LLM.

- **RAG Generation**
  - The retrieved context and your question are sent to the Ollama model.
  - The LLM generates a grounded answer that reflects your underlying documents.

- **Web UI Layer (Streamlit + Tailwind CSS v4)**
  - Streamlit handles user interaction (inputs, outputs, session state).
  - Tailwind CSS v4 powers the modern styling for the chat layout and controls.

You can customize the **retrieval strategy**, **chunk sizes**, and **prompt templates** in the Python code (primarily in `app.py` and related modules).

---

## 👨‍💻 Author

- Zain Abbas
- GitHub: https://github.com/zainabbas-se
- LinkedIn: https://www.linkedin.com/in/zainabbas-se/

If you use this project as a starter template or extend it, ⭐ **star the repo** and feel free to open issues or PRs!
