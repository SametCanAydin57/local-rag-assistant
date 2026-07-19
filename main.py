from chat import load_chat_model, answer_query


def main():
    """
    Starts the local RAG assistant application.

    Loads the local language model and
    handles user interaction through CLI.
    """

    print("Initializing RAG Assistant...")
    print("Loading local AI model, please wait...\n")


    # Load Phi-3.5 Mini local chat model
    model = load_chat_model()


    print("\nRAG Assistant ready!")
    print("Type 'exit' to quit.\n")


    while True:

        question = input("You: ").strip()


        # Prevent empty queries from reaching the embedding model
        if not question:
            print(
                "\nAssistant: Please enter a question.\n"
            )
            continue


        # Exit command
        if question.lower() == "exit":
            break


        answer_query(
            model,
            question
        )


if __name__ == "__main__":
    main()