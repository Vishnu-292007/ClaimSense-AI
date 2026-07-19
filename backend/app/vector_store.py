import faiss
import numpy as np

index = faiss.IndexFlatL2(384)

stored_chunks = []

def store_embeddings(embeddings, chunks):
    global stored_chunks

    embeddings = np.array(embeddings).astype("float32")

    index.add(embeddings)

    stored_chunks.extend(chunks)