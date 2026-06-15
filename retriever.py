import chromadb
from chromadb.utils import embedding_functions
from config import CHROMA_COLLECTION, CHROMA_PATH, EMBEDDING_MODEL, N_RESULTS


# Embedding function and ChromaDB client are initialized once at module load.
# sentence-transformers downloads the model on first use — this may take
# 30–60 seconds the very first time. Subsequent runs use a local cache.
print("Loading embedding model...")
_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)
print("Embedding model loaded.")
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(
    name=CHROMA_COLLECTION,
    embedding_function=_ef,
    metadata={"hnsw:space": "cosine"},
)


def get_collection():
    """Return the ChromaDB collection. Used by app.py during ingestion."""
    return collection

def embed_and_store(chunks):
    """
    Store chunks in ChromaDB.

    Embeddings are automatically generated using
    all-MiniLM-L6-v2 through ChromaDB's internal
    SentenceTransformer embedding function.
    """

    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:

        ids.append(
            f"{chunk['professor']}_{chunk['review_number']}"
        )

        documents.append(
            chunk["text"]
        )

        metadatas.append({
            "professor": chunk["professor"],
            "review_number": chunk["review_number"]
        })

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    print(
        f"Stored {len(chunks)} chunks in "
        f"'{CHROMA_COLLECTION}'."
    )

def retrieve(question, top_k=N_RESULTS):
    """
    Retrieve the top-k most relevant chunks
    using cosine similarity search.
    """

    results = collection.query(
        query_texts=[question],
        n_results=top_k
    )

    return results





