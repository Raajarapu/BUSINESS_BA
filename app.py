import streamlit as st
from config import APP_TITLE, CHUNK_SIZE, TOP_K

from ingestion.tabular import load_tabular, tabular_to_text
from ingestion.text import load_text
from ingestion.image import extract_text_from_image

from analytics.statistics import descriptive_statistics
from analytics.forecasting import forecast
from analytics.probability import monte_carlo

from rag.embeddings import embed_texts
from rag.vector_store import create_faiss_index
from rag.retrieval import retrieve

from llm.reasoning import reason

st.set_page_config(page_title=APP_TITLE, layout="wide")
st.title(APP_TITLE)

uploaded = st.file_uploader(
    "Upload CSV / Excel / Text / Image",
    type=["csv", "xlsx", "txt", "png", "jpg"]
)

if uploaded:
    text_data = ""

    if uploaded.name.endswith(("csv", "xlsx")):
        df = load_tabular(uploaded)
        st.dataframe(df.head())
        text_data = tabular_to_text(df)

        st.subheader("📊 Statistics")
        st.json(descriptive_statistics(df))

    elif uploaded.name.endswith("txt"):
        text_data = load_text(uploaded)

    else:
        text_data = extract_text_from_image(uploaded)

    chunks = [
        text_data[i:i+CHUNK_SIZE]
        for i in range(0, len(text_data), CHUNK_SIZE)
    ]

    embeddings = embed_texts(chunks)
    index = create_faiss_index(embeddings)

    st.subheader("🤖 Ask the Business Bot")
    question = st.text_input("Ask a business question")

    if question:
        context = retrieve(question, chunks, index, TOP_K)
        response = reason(" ".join(context), question)
        st.success(response)
