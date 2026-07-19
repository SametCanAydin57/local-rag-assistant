import json
import math
import os
import sqlite3

from foundry_local_sdk import FoundryLocalManager


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "rag.db")



def load_embeddings():
    """
    Loads stored document chunks and embeddings
    from the SQLite database.
    """

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
    SELECT source, content, embedding
    FROM documents
    """)

    rows = cursor.fetchall()

    connection.close()


    documents = []

    for row in rows:

        documents.append({
            "source": row[0],
            "content": row[1],
            "embedding": json.loads(row[2])
        })


    return documents



def cosine_similarity(vector1, vector2):
    """
    Calculates cosine similarity between two vectors.

    Higher score means the vectors are more
    semantically similar.
    """

    dot_product = sum(
        a * b
        for a, b in zip(vector1, vector2)
    )


    magnitude1 = math.sqrt(
        sum(value * value for value in vector1)
    )

    magnitude2 = math.sqrt(
        sum(value * value for value in vector2)
    )


    if magnitude1 == 0 or magnitude2 == 0:
        return 0


    return dot_product / (magnitude1 * magnitude2)



def get_top_chunks(
    query_embedding,
    documents,
    top_k=3,
    threshold=0.5,
    debug=False
):
    """
    Retrieves the most relevant document chunks
    based on cosine similarity scores.
    """

    results = []


    # Compare query embedding with all document embeddings
    for document in documents:

        score = cosine_similarity(
            query_embedding,
            document["embedding"]
        )


        if score >= threshold:

            results.append({
                "source": document["source"],
                "content": document["content"],
                "score": score
            })


    # Sort documents from most similar to least similar
    results.sort(
        key=lambda result: result["score"],
        reverse=True
    )


    # Avoid returning multiple chunks from the same source
    unique_results = []
    seen_sources = set()


    for result in results:

        if result["source"] not in seen_sources:

            unique_results.append(result)
            seen_sources.add(result["source"])


        if len(unique_results) == top_k:
            break



    if debug:

        print("\nRetrieval Results:")

        for result in unique_results:

            print(
                f"Source: {result['source']} | "
                f"Score: {result['score']:.4f}"
            )

        print()


    return unique_results



def generate_query_embedding(query):
    """
    Converts user query into an embedding vector
    using the local Qwen3 embedding model.
    """

    manager = FoundryLocalManager.instance


    embedding_model = manager.catalog.get_model(
        "qwen3-embedding-0.6b"
    )


    embedding_model.load()


    embedding_client = (
        embedding_model.get_embedding_client()
    )


    response = embedding_client.generate_embeddings(
        [query]
    )


    return response.data[0].embedding