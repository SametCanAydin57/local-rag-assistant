# Local RAG Assistant

A fully local **Retrieval-Augmented Generation (RAG)** assistant built with **Microsoft Foundry Local**, **Phi-3.5 Mini**, **Qwen3 Embedding Model**, and **SQLite**.

This project demonstrates an end-to-end RAG pipeline where documents are converted into embeddings, stored in a local database, retrieved using semantic similarity search, and used as context for a local language model to generate accurate answers.

---

# Overview

Large Language Models can generate impressive answers, but they may produce incorrect information when they do not have access to specific domain knowledge.

This project solves this problem using **Retrieval-Augmented Generation (RAG)**.

The system:

1. Loads local documents
2. Splits documents into smaller chunks
3. Converts text chunks into vector embeddings
4. Stores embeddings in SQLite
5. Retrieves the most relevant chunks using vector similarity
6. Provides retrieved context to a local LLM
7. Generates an answer based only on the provided information

---

# Architecture

```
Documents
    |
    v
Document Chunking
    |
    v
Embedding Generation
(Qwen3 Embedding 0.6B)
    |
    v
SQLite Embedding Storage
    |
    v
Semantic Retrieval
(Cosine Similarity Search)
    |
    v
Retrieved Context
    |
    v
Phi-3.5 Mini
(Local LLM)
    |
    v
Final Answer
```

---

# Features

* Fully local AI inference
* Retrieval-Augmented Generation pipeline
* Semantic search using embeddings
* SQLite-based knowledge storage
* Local LLM response generation
* Source citation for retrieved documents
* Context-based answering to reduce hallucinations
* CLI-based chat interface

---

# Technologies Used

## Programming Language

* Python 3.11

## AI Models

### Chat Model

**Phi-3.5 Mini**

Used for generating final responses based on retrieved context.

### Embedding Model

**Qwen3 Embedding 0.6B**

Used for converting text documents and user queries into vector representations.

## Database

**SQLite**

Used for storing:

* Document sources
* Text chunks
* Generated embeddings

## Framework

**Microsoft Foundry Local**

Used for running AI models locally without requiring cloud inference.

---

# Project Structure

```
rag_project/
│
├── main.py
│   └── Application entry point
│
├── chat.py
│   └── LLM integration and answer generation
│
├── retrieval.py
│   └── Vector search and similarity calculation
│
├── ingestion.py
│   └── Document processing and embedding generation
│
├── database.py
│   └── SQLite database operations
│
├── documents/
│   ├── rag_concepts.txt
│   ├── vector_search.txt
│   ├── embeddings.txt
│   └── other knowledge files
│
└── rag.db
    └── SQLite database containing document embeddings
```

---

# Installation

Requirements:

- Python 3.11+
- Microsoft Foundry Local
- Compatible local AI hardware

Install required dependencies:

```bash
pip install foundry-local-sdk
```

Make sure Microsoft Foundry Local is installed and available on your machine.

---

# Creating the Knowledge Base

Before running the assistant, documents must be processed.

Run:

```bash
python ingestion.py
```

This process will:

* Read documents from the `documents` folder
* Split documents into chunks
* Generate embeddings using Qwen3 Embedding
* Store data inside SQLite

Example output:

```
Total chunks: 6

Embedding generated.

[0] rag_concepts.txt
Embedding length:
1024
```

---

# Running the Assistant

Start the application:

```bash
python main.py
```

Example:

```
RAG Assistant ready!
Type 'exit' to quit.

You: What is RAG?

Assistant:
RAG stands for Retrieval-Augmented Generation, which is an AI framework that enhances a large language model's responses by dynamically retrieving relevant facts from external knowledge bases.

Sources:
- rag_concepts.txt (score: 0.5592)

---

# Example Queries

## Knowledge-based question

```
You:
What is vector search?
```

Response:

```
Vector search is a technique that retrieves
information based on semantic similarity between
embedding vectors.

Sources:
- vector_search.txt
```

---

## Unknown information

```
You:
Who is Albert Einstein?
```

Response:

```
I don't know based on the provided documents.
```

The assistant avoids generating unsupported answers because it is instructed to only use retrieved context.

---

# How Retrieval Works

For every user question:

1. The question is converted into an embedding vector.
2. The system compares this vector with stored document embeddings.
3. Cosine similarity is calculated.
4. The most relevant chunks are selected.
5. Selected chunks are provided as context to Phi-3.5 Mini.

---

# Responsible AI Considerations

The assistant follows several practices to reduce incorrect outputs:

* The model is instructed to answer only using retrieved context.
* Unknown information is rejected instead of hallucinated.
* Retrieved sources are displayed after each response.
* Local execution improves data privacy.

---
# Limitations

Current limitations of the system:

* The assistant only answers questions based on the provided documents.
* Retrieval quality depends on document chunking strategy.
* Local LLM inference can be slower compared to cloud-based models.
* The current implementation uses SQLite with manual cosine similarity search. For larger-scale applications, specialized vector databases could provide better scalability and performance.
* The application currently supports text documents only.

# Future Improvements

Possible extensions:

* Add Streamlit or Gradio web interface
* Support PDF and DOCX document ingestion
* Add conversation memory
* Replace SQLite search with FAISS or another vector database
* Improve chunking strategy
* Add metadata filtering
* Add multi-user support

---

# Author

Developed as a practical implementation of a local Retrieval-Augmented Generation system using Microsoft Foundry Local.
by Samet Can Aydın
