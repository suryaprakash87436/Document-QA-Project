# AI Document Q&A Chatbot — Gemini edition

This version uses Gemini for both chat generation and embeddings, with LangChain, FAISS, and Streamlit.

## Setup on Windows PowerShell

```powershell
cd "E:\GEN AI\document_qa_rag_gemini"
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

Paste your Google AI Studio key into `.env`:

```env
GEMINI_API_KEY=your_actual_Gemini_API_key
```

Save the file. Keep the key private; do not commit `.env` to GitHub.

## Run

```powershell
streamlit run app.py
```

Open the local URL shown in the terminal, usually http://localhost:8501.

## Important

- This app no longer calls OpenAI. Do not put a Gemini key in `OPENAI_API_KEY`.
- The app uses `gemini-embedding-2-preview` for embeddings and `gemini-2.5-flash` for chat. Model availability and free-tier quotas depend on your Google AI Studio project and region.
- If Google reports that the embedding model is unavailable, check the models enabled for your API key and select a supported embedding model in `app.py`.
- FAISS is stored in Streamlit session memory; reprocess documents after restarting the app.
- Scanned PDFs require OCR before text can be indexed.
