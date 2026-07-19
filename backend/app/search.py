from app.vector_store import index, stored_chunks
from app.embeddings import model
import numpy as np

def search(query, k=3):
    if len(stored_chunks) == 0:
        return ["No document uploaded."]

    query_embedding = model.encode([query]).astype("float32")

    k = min(k, len(stored_chunks))

    distances, indices = index.search(query_embedding, k)

    results = []

    for idx in indices[0]:
        if 0 <= idx < len(stored_chunks):
            results.append(stored_chunks[idx])

    return results