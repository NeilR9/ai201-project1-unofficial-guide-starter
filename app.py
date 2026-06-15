print("Starting app.py...")
from rag_pipeline import load_file_and_chunk_text
from retriever import embed_and_store, retrieve, get_collection

def run_ingestion():
    collection = get_collection()

    if collection.count() > 0:
        print(f"Vector store already populated ({collection.count()} chunks). Skipping ingestion.")
        print("To re-ingest, delete the ./chroma_db folder and restart.")
        return

    print("Ingesting data and creating chunks")
    chunks, profs = load_file_and_chunk_text("milestone1Doc")

    print("First chunks for FIrst 5 Profs:\n")
    for curProf in profs[0:5]:
        chunk = next(
            c for c in chunks
            if c["professor"] == curProf
        )
        print(f"Professor: {chunk['professor']}")
        print(f"Review #: {chunk['review_number']}")
        print(f"Text: {chunk['text']}")
        print("-" * 80)
    print(f"\nTotal Chunks Created: {len(chunks)}")
    if chunks:
        embed_and_store(chunks)

def chat(message):
    retrieved = []
    if not message.strip():
        return ""
    retrieved = retrieve(message)
    for i in range(len(retrieved["documents"][0])):
        print(f"\nResult {i+1}")
        print(
            f"Professor: "
            f"{retrieved['metadatas'][0][i]['professor']}"
        )
        print(
            f"Review #: "
            f"{retrieved['metadatas'][0][i]['review_number']}"
        )
        print(
            f"Distance: "
            f"{retrieved['distances'][0][i]:.3f}"
        )
        print(
            f"Text: "
            f"{retrieved['documents'][0][i]}"
        )
    
if __name__ == "__main__":
    print("\n" + "="*50)
    print("  Unofficial Guide — starting up")
    print("="*50 + "\n")
    run_ingestion()
    message = input("Enter a question: ")
    chat(message)
        