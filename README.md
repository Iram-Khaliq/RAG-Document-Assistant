# 📄 Document RAG Assistant

A backend-only Retrieval-Augmented Generation (RAG) application built using **FastAPI**, **OpenAI Embeddings**, and **ChromaDB**. This application allows users to upload PDF documents and ask questions based on the uploaded content.

> **Note:** The `uploads/` and `chroma_db/` directories are created automatically when the application runs for the first time.
Embeddings**, and **ChromaDB**. This application allows users to upload PDF documents and ask questions based on the uploaded content.

---

# 🚀 Features

* Upload PDF documents
* Extract text from PDFs
* Split text into chunks with overlap
* Generate semantic embeddings using OpenAI
* Store embeddings in ChromaDB
* Semantic similarity search
* AI-powered question answering
* REST APIs using FastAPI

---

# 🛠️ Technologies Used

* Python
* FastAPI
* OpenAI API
* ChromaDB
* PyPDF
* LangChain Text Splitters
* Python Dotenv

---

# 🏗️ Project Architecture

```text
                User
                  │
                  ▼
          Upload PDF / Ask Question
                  │
                  ▼
            FastAPI Backend
                  │
     ┌────────────┴────────────┐
     │                         │
     ▼                         ▼
OpenAI Embedding API       ChromaDB
     │                         │
     └────────────┬────────────┘
                  ▼
             ChatGPT Model
                  │
                  ▼
             Final Answer
```

---

#RAG-Project/

│
├── README.md
├── main.py
├── config.py
├── .env
├── requirements.txt
├── uploads/
└── chroma_db/

# ⚙️ Installation

## Clone Repository

```bash
git clone <repository-url>
cd RAG-Project
```

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
```

## Run the Application

```bash
uvicorn main:app --reload
```

API Documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🔄 Workflow

## 1. Upload PDF

* User uploads a PDF.
* The backend saves the PDF.
* Text is extracted using PyPDF.

## 2. Chunking

The extracted text is divided into smaller chunks using:

* Chunk Size: **1000**
* Chunk Overlap: **200**

This preserves context and improves retrieval accuracy.

## 3. Embedding Generation

Each chunk is converted into a semantic embedding using the OpenAI **text-embedding-3-small** model.

## 4. Store in ChromaDB

Each chunk is stored with:

* Unique ID
* Original Chunk
* Embedding
* Metadata (optional)

## 5. Question Answering

When a user asks a question:

1. The question is converted into an embedding.
2. ChromaDB performs semantic similarity search.
3. The most relevant chunks are retrieved.
4. Retrieved chunks are combined into a context.
5. The context and question are sent to the OpenAI Chat model.
6. The model generates the final answer.

---

# 📌 API Endpoints

## Home

```
GET /
```

Returns a welcome message.

---

## Upload PDF

```
POST /upload
```

Uploads a PDF, extracts text, generates embeddings, and stores the data in ChromaDB.

---

## Ask Question

```
POST /ask
```

Accepts a question and returns an AI-generated answer based on the uploaded document.

---

# 📈 Future Improvements

* Multiple document support
* Store page number metadata
* Source citations
* Document update/delete functionality
* Duplicate document detection
* Better error handling
* Authentication
* Docker deployment

---

# 📚 Learning Outcomes

This project demonstrates:

* FastAPI API Development
* PDF Processing
* Retrieval-Augmented Generation (RAG)
* OpenAI Embeddings
* Vector Database (ChromaDB)
* Semantic Search
* Prompt Engineering
* AI-powered Question Answering

---

# 👩‍💻 Author

**Iram Khaliq**

Software Engineer | MERN Stack Developer | AI Enthusiast
