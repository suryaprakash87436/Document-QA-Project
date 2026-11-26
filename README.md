
# AI Document Q&A Chatbot using RAG

An AI-powered document question-answering chatbot built using Retrieval-Augmented Generation (RAG).

## Features
- Upload PDF and TXT documents
- Extract and split document text
- Generate vector embeddings
- Search relevant document chunks using FAISS
- Generate answers using Groq AI
- Display source filenames and page numbers
- Interactive Streamlit interface

## Tech Stack
- Python
- Streamlit
- LangChain
- Groq API
- Hugging Face Embeddings
- FAISS
- Sentence Transformers
- PyPDF

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Live Demo

Try the deployed application here:

[AI Document Q&A Chatbot](https://document-app-project2.streamlit.app/)

## GitHub Repository

[View Source Code](https://github.com/suryaprakash87436/Document-QA-Project)

## Environment Variable

Set your Groq API key as `GROQ_API_KEY` in your environment or Streamlit secrets.

## Author
Surya Prakash
