from fastapi import FastAPI, UploadFile, File
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import shutil
import os

from prompts import RAG_SYSTEM_PROMPT
from config import client, collection


app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Welcome to RAG Project"
    }


# ==================================================
# Upload PDF
# ==================================================

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    # Create uploads folder
    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    # Save uploaded PDF
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Read PDF
    reader = PdfReader(file_path)

    text = ""

    # Extract text
    for page in reader.pages:
        extracted_text = page.extract_text()

        if extracted_text:
            text += extracted_text + "\n"

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_text(text)

    # -------------------------------------------------
    # Clear previous document from ChromaDB
    # -------------------------------------------------

    try:
        existing = collection.get()

        if existing["ids"]:
            collection.delete(ids=existing["ids"])

    except Exception:
        pass

    # -------------------------------------------------
    # Store chunks
    # -------------------------------------------------

    for index, chunk in enumerate(chunks):

        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk
        )

        embedding = response.data[0].embedding

        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[f"chunk_{index}"]
        )

    return {
        "message": "PDF uploaded successfully",
        "total_chunks": len(chunks)
    }


# ==================================================
# Ask Question
# ==================================================

@app.post("/ask")
async def ask_question(question: str):

    # Create embedding for user question
    question_response = client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    )

    question_embedding = question_response.data[0].embedding

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=5
    )

    # Combine retrieved chunks
    context = "\n".join(results["documents"][0])

    # Debug
    print("=" * 60)
    print("Retrieved Context:\n")
    print(context)
    print("=" * 60)

    # Create prompt
    prompt = f"""
Context:
{context}

Question:
{question}

Answer ONLY from the provided context.

If the answer is not available in the context, reply:

"I don't know based on the uploaded document."
"""

    # Ask ChatGPT
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": RAG_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Get final answer
    answer = response.choices[0].message.content

    return {
        "question": question,
        "answer": answer
    }