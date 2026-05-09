import streamlit as st

st.set_page_config(
    page_title="BioCert RAG Demo",
    page_icon="🧬",
    layout="centered"
)

DEMO_CORPUS = [
    {
        "title": "Organic certification procedure",
        "source": "Demo knowledge base / Certification workflow",
        "text": (
            "Organic certification normally involves an application by the producer, "
            "registration with a control body, submission of farm and parcel information, "
            "review of production practices, an inspection, assessment of non-conformities, "
            "and issuance or renewal of certification if the requirements are met."
        ),
    },
    {
        "title": "Conversion period",
        "source": "Demo knowledge base / Organic production principles",
        "text": (
            "A conversion period is usually required before products can be marketed as organic. "
            "During this period, the producer must follow organic production rules, while the land "
            "and production system are monitored before full organic status is granted."
        ),
    },
    {
        "title": "Allowed inputs",
        "source": "Demo knowledge base / Farm inputs",
        "text": (
            "Organic farming restricts the use of synthetic fertilizers and pesticides. "
            "Allowed inputs may include approved organic fertilizers, compost, manure, certain minerals, "
            "and plant protection products specifically permitted under organic rules."
        ),
    },
    {
        "title": "Inspection and control",
        "source": "Demo knowledge base / Control system",
        "text": (
            "Organic certification is based on documentary checks, farm inspections, traceability records, "
            "input invoices, production logs, and verification that the producer follows the applicable rules."
        ),
    },
    {
        "title": "Remote sensing support",
        "source": "Demo knowledge base / Earth observation",
        "text": (
            "Remote sensing can support organic certification by monitoring parcel-level vegetation patterns, "
            "land cover, crop condition, and possible inconsistencies. It cannot replace certification decisions, "
            "but it can provide additional evidence for risk-based inspection."
        ),
    },
]


def retrieve(question: str, top_k: int = 3):
    q_words = set(question.lower().replace(",", " ").replace(".", " ").split())

    scored = []
    for doc in DEMO_CORPUS:
        text = (doc["title"] + " " + doc["text"]).lower()
        score = sum(1 for w in q_words if w in text)
        scored.append((score, doc))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for score, doc in scored[:top_k] if score > 0]


def generate_demo_answer(question: str, docs):
    if not docs:
        return (
            "I could not find a relevant passage in the demo knowledge base. "
            "In the full version, the system would search the complete BioCert RAG corpus."
        )

    answer = (
        "Based on the retrieved demo sources, organic certification generally involves "
        "registration with a control body, submission of farm and parcel information, "
        "inspection of the production system, review of records and inputs, and a certification "
        "decision after any non-conformities are assessed."
    )

    if any("remote sensing" in d["title"].lower() for d in docs):
        answer += (
            " Remote sensing can support this process as an additional monitoring layer, "
            "but it should not replace documentary checks, inspections, or expert judgement."
        )

    return answer


st.title("🧬 BioCert RAG Demo")
st.caption("Research prototype for organic certification question answering")

st.info(
    "This is a public demo interface with a small built-in demo corpus. "
    "The full RAG corpus can later be connected from a private data repository."
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
        docs = retrieve(question)
        answer = generate_demo_answer(question, docs)

        st.write("### Demo answer")
        st.write(answer)

        st.write("### Retrieved demo sources")
        if docs:
            for i, doc in enumerate(docs, start=1):
                with st.expander(f"{i}. {doc['title']}"):
                    st.write(doc["text"])
                    st.caption(doc["source"])
        else:
            st.info("No matching demo source found.")

        st.write("### Your question")
        st.code(question)

st.divider()

st.caption(
    "Research prototype. Not a legal authority, certification body, or official advisory system."
)