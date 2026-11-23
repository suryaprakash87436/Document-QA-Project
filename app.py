
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_ollama import OllamaEmbeddings
from src.rag import build_vector_store, answer_question

load_dotenv()

st.set_page_config(
    page_title="AI Document Q&A",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Document Q&A Chatbot")
st.caption("Upload PDF or TXT files and ask questions grounded in their content.")

# Check Groq API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY is missing. Add it to your .env file and restart Streamlit.")
    st.stop()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("1. Upload documents")

    uploads = st.file_uploader(
        "Choose PDF or TXT files",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )

    chunk_size = st.slider("Chunk size", 300, 2000, 1000, 100)
    chunk_overlap = st.slider("Chunk overlap", 0, 400, 150, 25)

    model_name = st.text_input(
        "Groq chat model",
        value="openai/gpt-oss-120b"
    )

    process = st.button(
        "Process documents",
        type="primary",
        use_container_width=True
    )

    st.divider()

    if st.button("Clear chat and documents", use_container_width=True):
        for key in ("vector_store", "document_names", "messages"):
            st.session_state.pop(key, None)
        st.rerun()

# Process uploaded documents
if process:
    if not uploads:
        st.warning("Upload at least one PDF or TXT file first.")
    else:
        try:
            with st.spinner("Reading, chunking, embedding, and indexing documents..."):

                # Local Ollama embeddings
                embeddings = OllamaEmbeddings(
                    model="nomic-embed-text"
                )

                store, names, chunk_count = build_vector_store(
                    uploads,
                    embeddings,
                    chunk_size,
                    chunk_overlap
                )

                st.session_state.vector_store = store
                st.session_state.document_names = names
                st.session_state.messages = []

            st.success(
                f"Indexed {len(names)} file(s) into {chunk_count} chunks."
            )

        except Exception as exc:
            st.error(f"Could not process documents: {exc}")

# Show indexed documents
if st.session_state.get("document_names"):
    st.sidebar.success(
        "Indexed: " + ", ".join(st.session_state.document_names)
    )

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        if msg.get("sources"):
            with st.expander("Sources used"):
                for source in msg["sources"]:
                    st.write(
                        f"**{source['file']}** — page {source['page']}"
                    )
                    st.caption(source["excerpt"])

# Chat interface
if not st.session_state.get("vector_store"):
    st.info(
        "Upload documents in the sidebar, then click **Process documents**."
    )

else:
    question = st.chat_input(
        "Ask a question about your uploaded documents..."
    )

    if question:
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        try:
            with st.chat_message("assistant"):
                with st.spinner(
                    "Searching documents and generating an answer..."
                ):

                    # Groq LLM
                    llm = ChatGroq(
                        model=model_name,
                        temperature=0,
                        api_key=api_key
                    )

                    result = answer_question(
                        question=question,
                        vector_store=st.session_state.vector_store,
                        llm=llm,
                        chat_history=st.session_state.messages[:-1]
                    )

                    st.markdown(result["answer"])

                    if result["sources"]:
                        with st.expander("Sources used", expanded=True):
                            for source in result["sources"]:
                                st.write(
                                    f"**{source['file']}** — page {source['page']}"
                                )
                                st.caption(source["excerpt"])

            st.session_state.messages.append({
                "role": "assistant",
                "content": result["answer"],
                "sources": result["sources"]
            })

        except Exception as exc:
            st.error(f"Something went wrong while answering: {exc}")
