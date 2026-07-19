import os

from foundry_local_sdk import Configuration, FoundryLocalManager

from database import (
    create_database,
    insert_documents
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_PATH = os.path.join(BASE_DIR, "documents")


def load_documents():
    """
    Loads text documents from the documents folder.
    """

    documents = []

    for filename in os.listdir(DOCS_PATH):

        filepath = os.path.join(
            DOCS_PATH,
            filename
        )

        with open(filepath, "r", encoding="utf-8") as file:

            documents.append({
                "filename": filename,
                "content": file.read()
            })

    return documents



def chunk_text(text):
    """
    Splits documents into smaller chunks.

    Current strategy:
    Paragraph-based chunking using empty lines.
    """

    chunks = text.split("\n\n")

    # Remove empty chunks and unnecessary spaces
    chunks = [
        chunk.strip()
        for chunk in chunks
        if chunk.strip()
    ]

    return chunks



def process_documents():
    """
    Converts documents into smaller chunks
    that can be converted into embeddings.
    """

    documents = load_documents()

    all_chunks = []

    for document in documents:

        chunks = chunk_text(
            document["content"]
        )

        for chunk in chunks:

            all_chunks.append({
                "source": document["filename"],
                "text": chunk
            })

    return all_chunks



def generate_embeddings(chunks):
    """
    Generates embeddings for document chunks
    using the local Qwen3 embedding model.
    """

    config = Configuration(
        app_name="rag_project"
    )

    FoundryLocalManager.initialize(config)

    manager = FoundryLocalManager.instance


    embedding_model = manager.catalog.get_model(
        "qwen3-embedding-0.6b"
    )


    # Download model if it is not available locally
    embedding_model.download(
        lambda progress: print(
            f"\rDownloading embedding model: {progress:.1f}%",
            end="",
            flush=True
        )
    )

    print()


    embedding_model.load()

    embedding_client = (
        embedding_model.get_embedding_client()
    )


    texts = [
        chunk["text"]
        for chunk in chunks
    ]


    response = embedding_client.generate_embeddings(
        texts
    )


    # Attach generated vectors to corresponding chunks
    for chunk, embedding in zip(
        chunks,
        response.data
    ):
        chunk["embedding"] = embedding.embedding


    return chunks



if __name__ == "__main__":

    chunks = process_documents()

    print(
        f"Total chunks: {len(chunks)}"
    )


    chunks = generate_embeddings(
        chunks
    )


    create_database()

    insert_documents(
        chunks
    )


    print("\nEmbeddings generated and stored.\n")