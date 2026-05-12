# 🤖 RAG Document Q&A Chatbot

An AI-powered chatbot that lets you upload any PDF and ask questions about it in plain English — powered by **Retrieval-Augmented Generation (RAG)**.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green)
![Gemini](https://img.shields.io/badge/Google-Gemini-orange?logo=google)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?logo=streamlit)
![FAISS](https://img.shields.io/badge/FAISS-VectorStore-purple)

---

## ✨ Features

- 📄 Upload any PDF document through a clean web interface
- 💬 Ask questions in plain English and get accurate, grounded answers
- 🔍 Semantic search over document content using FAISS vector store
- 📌 Source citations with page numbers for every answer
- 🧠 Conversation memory — follow-up questions are context-aware
- ⚡ Fast responses powered by Gemini 2.0 Flash

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| LLM & Embeddings | Google Gemini API (`gemini-2.0-flash`, `gemini-embedding-001`) |
| RAG Orchestration | LangChain |
| Vector Store | FAISS |
| PDF Parsing | PyPDFLoader |
| Web UI | Streamlit |
| Language | Python |

---

## 🏗️ Architecture

```
PDF Upload → PyPDFLoader → RecursiveCharacterTextSplitter
         → Gemini Embeddings → FAISS Vector Store
User Query → Semantic Retrieval (top-4 chunks) → Gemini LLM → Answer + Sources
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.9+
- A [Google AI Studio](https://aistudio.google.com/) API key (free tier available)

  ### 1. Clone the repository

  ```bash
  git clone https://github.com/Harsha77064/rag-chatbot.git
  cd rag-chatbot
  ```

  ### 2. Install dependencies

  ```bash
  pip install -r requirements.txt
  ```

  ### 3. Configure your API key

  Create a `.env` file in the project root:

  ```bash
  GOOGLE_API_KEY=your_api_key_here
  ```

  > ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

  ### 4. Run the app

  ```bash
  streamlit run app.py
  ```

  Open your browser at `http://localhost:8501`.

  ---

  ## 🚀 Usage

  1. **Upload** a PDF using the sidebar file uploader
  2. Wait for the document to be processed (chunk count and page count will be shown)
  3. **Ask** any question in the chat input
  4. View the **answer** along with expandable **source excerpts** and page numbers
  5. Ask follow-up questions — the chatbot remembers the conversation
  6. Click **Upload New PDF** to start fresh with a different document
 
  7. ---
 
  8. ## 📁 Project Structure
 
  9. ```
     rag-chatbot/
     ├── app.py              # Main Streamlit application
     ├── requirements.txt    # Python dependencies
     ├── .env                # API key (do NOT commit this)
     ├── .gitignore          # Excludes .env and other sensitive files
     └── README.md
     ```

     ---

  
