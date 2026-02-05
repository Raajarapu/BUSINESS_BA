import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd

from config import APP_TITLE, CHUNK_SIZE, TOP_K

from ingestion.tabular import load_tabular, tabular_to_text
from ingestion.text import load_text
from ingestion.image import extract_text_from_image


from analysis.statistics import descriptive_statistics, correlation_analysis
from analysis.forecasting import forecast
from analysis.probability import monte_carlo


from rag.embeddings import embed_texts
from rag.vector_store import create_faiss_index
from rag.retrieval import retrieve

from llm.reasoning import reason


# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title=APP_TITLE, layout="wide")
st.title(APP_TITLE)
st.caption("📊 Statistical • 📈 Forecasting • 🎲 Probability • 🤖 Business Reasoning")

# ------------------ SIDEBAR ------------------
st.sidebar.header("📂 Upload Data")
uploaded = st.sidebar.file_uploader(
    "Upload CSV / Excel / Text / Image",
    type=["csv", "xlsx", "txt", "png", "jpg"]
)

st.sidebar.info(
    "Workflow:\n"
    "1. Upload data\n"
    "2. Explore analysis tabs\n"
    "3. Ask business questions"
)

# ------------------ MAIN LOGIC ------------------
if not uploaded:
    st.warning("👈 Upload a file to start analysis")
    st.stop()

text_data = ""
df = None

# -------- FILE HANDLING --------
if uploaded.name.endswith(("csv", "xlsx")):
    df = load_tabular(uploaded)
    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    text_data = tabular_to_text(df)

elif uploaded.name.endswith("txt"):
    text_data = load_text(uploaded)

else:
    text_data = extract_text_from_image(uploaded)

# -------- TEXT CHUNKING + RAG --------
chunks = [
    text_data[i:i + CHUNK_SIZE]
    for i in range(0, len(text_data), CHUNK_SIZE)
]

embeddings = embed_texts(chunks)
index = create_faiss_index(embeddings)

# ------------------ TABS ------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Statistics", "📈 Forecasting", "🎲 Probability", "🤖 Business Bot"]
)

# ------------------ TAB 1: STATISTICS ------------------
with tab1:
    st.header("Descriptive Statistics & Correlation")

    if df is not None:
        st.subheader("📊 Descriptive Statistics")
        st.json(descriptive_statistics(df))

        st.subheader("🔗 Correlation Matrix")
        st.json(correlation_analysis(df))
    else:
        st.info("Statistics available only for tabular data.")

# ------------------ TAB 2: FORECASTING ------------------
with tab2:
    st.header("Time-Series Forecasting")

    if df is not None:
        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        if numeric_cols:
            col = st.selectbox("Select column to forecast", numeric_cols)
            steps = st.slider("Forecast periods", 3, 24, 6)

            forecast_values = forecast(df[col], steps)
            st.success(f"Forecast for next {steps} periods:")
            st.write(forecast_values)
        else:
            st.warning("No numeric columns available.")
    else:
        st.info("Forecasting available only for tabular data.")

# ------------------ TAB 3: PROBABILITY ------------------
with tab3:
    st.header("Probability & Risk Analysis")

    if df is not None:
        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        if numeric_cols:
            col = st.selectbox("Select column for simulation", numeric_cols)
            sims = st.slider("Number of simulations", 100, 5000, 1000)

            sim_data = monte_carlo(df[col], sims)
            st.success("Monte Carlo Simulation Complete")
            st.write(sim_data[:20])
        else:
            st.warning("No numeric columns available.")
    else:
        st.info("Probability analysis available only for tabular data.")

# ------------------ TAB 4: BUSINESS BOT ------------------
with tab4:
    st.header("Business Model Evaluation Bot")

    question = st.text_input(
        "Ask a business question (strategy, risk, performance, insights)"
    )

    if question:
        context = retrieve(question, chunks, index, TOP_K)
        answer = reason(" ".join(context), question)

        st.subheader("📌 Insight")
        st.success(answer)
