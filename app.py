#print("Starting app.py...")
import gradio as gr
from rag_pipeline import load_file_and_chunk_text
from retriever import embed_and_store, retrieve, get_collection
from generator import generate_response

def run_ingestion():
    collection = get_collection()

    if collection.count() > 0:
        print(f"Vector store already populated ({collection.count()} chunks). Skipping ingestion.")
        print("To re-ingest, delete the ./chroma_db folder and restart.")
        return
    
    chunks, profs = load_file_and_chunk_text("milestone1Doc")

    print("First chunks for First 5 Profs:\n")
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

def chat(message, history):
    """
    Called by Gradio whenever the user submits a question.
    """
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
        print(
            f"Source: "
            f"{retrieved['metadatas'][0][i]["source"]}"
        )
    
    result = generate_response(message, retrieved)

    source_text = "\n".join(
    f"• {source}"
    for source in result["sources"]
    )

    return (
        f"{result['answer']}\n\n"
        f"### Sources Used\n"
        f"{source_text}"
    )


def create_ui():

    with gr.Blocks(
        title="ASU CS Professor Guide"
    ) as demo:

        # --------------------------------------------------
        # Header
        # --------------------------------------------------

        gr.HTML("""
        <div style="text-align:center; padding:1.25rem 0 0.5rem;">
            <h1 style="
                font-size:2rem;
                font-weight:700;
                color:#1e3a8a;
                margin:0;">
                🎓 ASU CS Professor Guide
            </h1>

            <p style="
                color:#6b7280;
                font-size:1rem;
                margin:0.4rem 0 0;">
                Ask anything about ASU Computer Science professors
                using real student reviews.
            </p>
        </div>
        """)

        with gr.Row():

            # --------------------------------------------------
            # Chat Interface
            # --------------------------------------------------

            with gr.Column(scale=3):

                gr.ChatInterface(
                    fn=chat,

                    chatbot=gr.Chatbot(
                        height=500,
                        placeholder=(
                            "<div style='text-align:center;"
                            "color:#9ca3af;"
                            "margin-top:3rem;'>"
                            "Ask a question about an ASU CS professor 🎓"
                            "</div>"
                        ),
                    ),

                    textbox=gr.Textbox(
                        placeholder='e.g. "Which professor is most approachable?"',
                        container=False,
                        scale=7,
                    ),

                    examples=[
                        "Which professor receives most praise for explaining challenging concepts in a clear manner?",
                        "Which professor is frequently described as approachable and supportive, especially when being able to help students outside class?",
                        "Which professor receives the most complaints about their curriculum and being difficult with hard or unfair exams?",
                        "Which professor is most often criticized for their coursework in terms of excessive workload or too much reading or course structure?",
                        "Which professor appears to leave the best overall impression on students?",
                        "Which professor receives the most student reviews that describe any course they taught as both difficult and rewarding?"
                    ],

                    cache_examples=False,
                )

            # --------------------------------------------------
            # Sidebar
            # --------------------------------------------------

            with gr.Column(
                scale=1,
                min_width=220
            ):

                gr.HTML("""
                <div style="
                    background:#eff6ff;
                    border:1px solid #bfdbfe;
                    border-radius:10px;
                    padding:1rem;
                    margin-top:0.5rem;">

                    <p style="
                        font-size:0.8rem;
                        font-weight:700;
                        color:#1e3a8a;
                        margin:0 0 0.5rem;">
                        📚 LOADED PROFESSORS
                    </p>

                    <ul style="
                        font-size:0.85rem;
                        color:#1e40af;
                        list-style:none;
                        padding:0;
                        margin:0;
                        line-height:1.8;">

                        <li>👨‍🏫 Joshua Daymude</li>
                        <li>👨‍🏫 Ryan Meuth</li>
                        <li>👨‍🏫 David Claveau</li>
                        <li>👨‍🏫 Ming Zhao</li>
                        <li>👨‍🏫 James Gordon</li>
                        <li>👨‍🏫 Justin Selgrad</li>
                        <li>👩‍🏫 Farideh Tadayon-Navabi</li>
                        <li>👩‍🏫 Xuerong Feng</li>
                        <li>👨‍🏫 Subbarao Kambhampati</li>
                        <li>👨‍🏫 Bharatesh Chakravarthi</li>

                    </ul>

                    <hr style="
                        border:none;
                        border-top:1px solid #bfdbfe;
                        margin:0.75rem 0;">
                </div>
                """)

    return demo
    
if __name__ == "__main__":
    print("\n" + "="*50)
    print("  Unofficial Guide — starting up")
    print("="*50 + "\n")
    run_ingestion()
    demo = create_ui()

    print("Launching Gradio UI...")

    demo.launch(
        theme=gr.themes.Soft(
            primary_hue="blue"
        )
    )
        