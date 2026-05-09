import streamlit as st

st.set_page_config(
    page_title="BioCert RAG Demo",
    page_icon="🧬",
    layout="centered"
)

st.title("🧬 BioCert RAG Demo")
st.caption("Research prototype for organic certification question answering")

st.info(
    "This is a public demo interface. "
    "The full RAG corpus can be connected later from a private data repository."
)

st.subheader("Ask a question")

question = st.text_input(
    "Question",
    placeholder="e.g. What is required for organic crop production?"
)

if st.button("Submit"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        st.write("### Prototype response")
        st.write(
            "This demo is currently connected only to the interface layer. "
            "In the next step, it will retrieve documents from the BioCert RAG corpus "
            "and generate source-grounded answers."
        )

        st.write("### Your question")
        st.code(question)

st.divider()

st.caption(
    "Research prototype. Not a legal authority, certification body, or official advisory system."
)