import pandas as pd

def load_tabular(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    elif file.name.endswith(".xlsx"):
        return pd.read_excel(file)
    else:
        raise ValueError("Unsupported tabular format")

def tabular_to_text(df: pd.DataFrame) -> str:
    text = ""
    for col in df.columns:
        values = df[col].astype(str).tolist()[:20]
        text += f"{col}: {values}\n"
    return text
