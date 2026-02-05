import numpy as np
from rag.embeddings import embed_texts

def retrieve(query, chunks, index, top_k=3):
    query_vec = embed_texts([query])
    _, indices = index.search(np.array(query_vec), top_k)
    return [chunks[i] for i in indices[0]]
