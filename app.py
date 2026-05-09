import re
from pathlib import Path

import streamlit as st
from pypdf import PdfReader


st.set_page_config(
    page_title="BioCert RAG Demo",
    page_icon="🧬",
    layout="centered",
)

DATA_DIR = Path("data")


@st.cache_data(show_spinner=True)
def load_pdf_corpus():
    documents = []

    if not DATA_DIR.exists():
        return documents

    pdf_files = sorted(DATA_DIR.glob("*.pdf"))

    for pdf_path in pdf_files:
        try:
            reader = PdfReader(str(pdf_path))
            for page_number, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                text = re.sub(r"\s+", " ", text).strip()

                if len(text) > 80:
                    documents.append(
                        {
                            "file": pdf_path.name,
                            "page": page_number,
                            "text": text,
                        }
                    )
        except Exception as e:
            documents.append(
                {
                    "file": pdf_path.name,
                    "page": "-",
                    "text": f"Could not read this PDF: {e}",
                }
            )

    return documents


def tokenize(text: str):
    text = text.lower()
    text = re.sub(r"[^a-zA-Zα-ωΑ-Ω0-9]+", " ", text)
    return [w for w in text.split() if len(w) > 2]


def retrieve(question: str, documents, top_k: int = 5):
    q_words = set(tokenize(question))

    scored = []
    for doc in documents:
        text_word_set = set(tokenize(doc["text"]))
        overlap = len(q_words.intersection(text_word_set))
        score = overlap

        if score > 0:
            scored.append((score, doc))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]


def make_snippet(text: str, question: str, max_chars: int = 1100):
    words = tokenize(question)
    lower_text = text.lower()
    best_pos = 0

    for w in words:
        pos = lower_text.find(w.lower())
        if pos != -1:
            best_pos = max(0, pos - 300)
            break

    snippet = text[best_pos : best_pos + max_chars]

    if best_pos > 0:
        snippet = "..." + snippet
    if best_pos + max_chars < len(text):
        snippet = snippet + "..."

    return snippet


st.title("🧬 BioCert RAG Demo")
st.caption("Online research prototype for organic certification document retrieval")

st.info(
    "This version searches real PDF documents included in the demo corpus. "
    "It retrieves relevant passages, but it does not yet use an LLM to generate final answers."
)

documents = load_pdf_corpus()

with st.sidebar:
    st.header("Corpus")
    st.write(f"PDF pages loaded: **{len(documents)}**")

    if DATA_DIR.exists():
        pdf_files = sorted(DATA_DIR.glob("*.pdf"))
        if pdf_files:
            for pdf in pdf_files:
                st.write(f"• {pdf.name}")
        else:
            st.warning("No PDF files found in the data folder.")
    else:
        st.warning("No data folder found.")

st.subheader("Ask a question")

question = st.text_input(
    "Question",
    placeholder="e.g. What is required for organic crop production?",
)

top_k = st.slider("Number of retrieved passages", min_value=1, max_value=10, value=5)

if st.button("Search"):
    if not question.strip():
        st.warning("Please enter a question.")
    elif not documents:
        st.error("No PDF corpus loaded. Add PDF files inside the data folder.")
    else:
        results = retrieve(question, documents, top_k=top_k)

        if not results:
            st.warning("No relevant passage found in the current PDF corpus.")
        else:
            st.write("### Retrieved passages")

            for i, (score, doc) in enumerate(results, start=1):
                title = f"{i}. {doc['file']} — page {doc['page']}"

                with st.expander(title, expanded=(i == 1)):
                    st.caption(f"Retrieval score: {score}")
                    st.write(make_snippet(doc["text"], question))

            st.write("### Interpretation")
            st.write(
                "The passages above are retrieved from the uploaded PDF corpus. "
                "A later version can use an LLM to synthesize these passages into a "
                "source-grounded answer with citations."
            )

st.divider()

st.caption(
    "Research prototype. Not a legal authority, certification body, or official advisory system."
)