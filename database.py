import json
import os
import sqlite3


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "rag.db")


def create_database():
    """
    Creates the SQLite database table used for storing
    document chunks and their embeddings.
    """

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        content TEXT,
        embedding TEXT
    )
    """)

    connection.commit()
    connection.close()


def clear_documents():
    """
    Removes all stored documents from the database.
    Used when rebuilding the knowledge base.
    """

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
    DELETE FROM documents
    """)

    connection.commit()
    connection.close()


def insert_documents(chunks):
    """
    Inserts processed document chunks and their embeddings
    into the SQLite database.
    """

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    for chunk in chunks:

        # Embeddings are stored as JSON text because
        # SQLite does not have a native vector data type.
        embedding_json = json.dumps(
            chunk["embedding"]
        )

        cursor.execute("""
        INSERT INTO documents(
            source,
            content,
            embedding
        )
        VALUES (?, ?, ?)
        """,
        (
            chunk["source"],
            chunk["text"],
            embedding_json
        ))

    connection.commit()
    connection.close()


if __name__ == "__main__":

    create_database()

    print("Database created.")