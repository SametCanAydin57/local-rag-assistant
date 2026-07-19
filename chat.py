import time

from foundry_local_sdk import Configuration, FoundryLocalManager

from retrieval import (
    load_embeddings,
    generate_query_embedding,
    get_top_chunks
)


def load_chat_model():
    """
    Initializes the local language model using Microsoft Foundry Local.
    Returns a chat client for generating responses.
    """

    config = Configuration(app_name="rag_project")

    FoundryLocalManager.initialize(config)

    manager = FoundryLocalManager.instance

    chat_model = manager.catalog.get_model(
        "phi-3.5-mini"
    )

    chat_model.load()

    return chat_model.get_chat_client()


def answer_query(model, question):
    """
    Handles the complete RAG pipeline:
    1. Load stored document embeddings
    2. Generate embedding for user query
    3. Retrieve relevant document chunks
    4. Generate answer using local LLM
    """

    start_time = time.time()

    # Load document embeddings from SQLite database
    documents = load_embeddings()

    # Convert user question into an embedding vector
    query_embedding = generate_query_embedding(
        question
    )

    # Retrieve the most relevant document chunks
    results = get_top_chunks(
        query_embedding,
        documents,
        top_k=2,
        debug=False
    )

    # Handle cases where no relevant information is found
    if not results:

        end_time = time.time()

        print("\nAssistant: No relevant documents found.")
        print("Try asking a more specific question.")

        print(
            f"Response time: {end_time - start_time:.2f} seconds\n"
        )

        return


    # Combine retrieved chunks into a single context
    context = "\n\n".join(
        result["content"]
        for result in results
    )


    # Prompt ensures that the model only uses retrieved information
    # and avoids hallucinating unsupported answers.
    prompt = f"""
You are a helpful AI assistant.

Answer the user's question only using the provided context.
If the answer is not in the context, say you don't know.

Context:
{context}

Question:
{question}
"""


    messages = [
        {
            "role": "system",
            "content": "You answer questions using provided context."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]


    print("\nAssistant: ", end="", flush=True)

    full_response = ""


    # Stream model response token by token
    for chunk in model.complete_streaming_chat(messages):

        if not chunk.choices:
            continue

        content = chunk.choices[0].delta.content

        if content:
            print(content, end="", flush=True)
            full_response += content


    print("\n")

    # Display retrieved sources and similarity scores
    print("Sources:")

    for result in results:
        print(
            f"- {result['source']} (score: {result['score']:.4f})"
        )


    end_time = time.time()

    print(
        f"Response time: {end_time - start_time:.2f} seconds"
    )

    return full_response