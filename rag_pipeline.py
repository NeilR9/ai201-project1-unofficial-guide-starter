import os
import re


def load_file_and_chunk_text(folder_path):
    """
    Loads all the .txt documents from the milestone1Doc directory
    professor review documents. 
    Splits a document into chunks where fixed-size chunking is used by
    treating each review below a Review Marker(Review 1, Review 2, etc..) as one chunk 


    Strategy: Use Parsing and Pattern Matching using regular expressions to extract professor name and review.
    Use fixed-size chunking where we consider one review as a single chunk. 
      - Chunk boundaries are determined by review markers
        (Review 1, Review 2, etc.).
    - Overlap = 0.
    - Chunk size varies naturally based on review length,
    approximately 20-90 tokens.

    Returns a list of chunk dictionaries where each dictionary cosists of 
      - "professor"     : the professor name(str)
      - "review_number" : the review number(int)
      - "text"          : the review or chunk(str)         
    """

    chunks = []
    professors = []

    # Process all txt files
    for filename in os.listdir(folder_path):

        if not filename.endswith(".txt"):
            continue

        file_path = os.path.join(folder_path, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        # Extract professor name
        professor_match = re.search(
            r"Professor:\s*(.+)",
            text
        )

        professor_name = (
            professor_match.group(1).strip()
            if professor_match
            else "Unknown"
        )
        if professor_name != "Unknown":
            professors.append(professor_name)

        # Extract all reviews
        # Captures everything after "Review X:"
        # until the next Review or end of file
        review_pattern = re.compile(
            r"Review\s+(\d+):\s*(.*?)(?=Review\s+\d+:|$)",
            re.DOTALL
        )

        reviews = review_pattern.findall(text)

        for review_num, review_text in reviews:

            review_text = review_text.strip()

            if review_text:
                chunks.append({
                    "professor": professor_name,
                    "review_number": int(review_num),
                    "text": review_text
                })

    return chunks, professors


# Example usage
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

"""
for i, chunk in enumerate(chunks[:5], start=1):
    print(f"Chunk {i}")
    print(f"Professor: {chunk['professor']}")
    print(f"Review #: {chunk['review_number']}")
    print(f"Text: {chunk['text']}")
    print("-" * 80)
"""
print(f"\nTotal Chunks Created: {len(chunks)}")