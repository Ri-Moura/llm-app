import os
from typing import List
from pinecone import Pinecone, ServerlessSpec
from app.services.openai_service import get_embedding

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
pc = Pinecone(api_key=PINECONE_API_KEY)

EMBEDDING_DIMENSION = 1536

def embed_chunks_and_upload_to_pinecone(chunks: List[str], index_name: str) -> None:
    """
    Embed text chunks using OpenAI and upload them to Pinecone.

    Args:
        chunks (List[str]): The list of text chunks to be embedded.
        index_name (str): The name of the Pinecone index.
    """
    if index_name in pc.list_indexes().names():
        print("\nIndex already exists. Will not create again!")
    else:
        print("\nIndex not exists")
        print("\nCreating a new index: ", index_name)
        pc.create_index(
            name=index_name,
            dimension=EMBEDDING_DIMENSION,
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )

        index = pc.Index(index_name)

        print("\nEmbedding chunks using OpenAI ...")
        embeddings_with_ids = [(str(i), get_embedding(chunk), chunk) for i, chunk in enumerate(chunks)]

        print("\nUploading chunks to Pinecone ...")
        upserts = [(id, vec, {"chunk_text": text}) for id, vec, text in embeddings_with_ids]
        index.upsert(vectors=upserts)

        print(f"\nUploaded {len(chunks)} chunks to Pinecone index '{index_name}'.")

def get_most_similar_chunks_for_query(query: str, index_name: str) -> List[str]:
    """
    Get the most similar text chunks for a given query from Pinecone.

    Args:
        query (str): The query to find similar chunks for.
        index_name (str): The name of the Pinecone index.

    Returns:
        List[str]: A list of the most similar text chunks.
    """
    print("\nEmbedding query using OpenAI ...")
    question_embedding = get_embedding(query)

    print("\nQuerying Pinecone index ...")
    index = pc.Index(index_name)
    query_results = index.query(vector=question_embedding, top_k=3, include_metadata=True)

    if not query_results['matches']:
        print("No matches found in Pinecone index.")
    context_chunks = [x['metadata']['chunk_text'] for x in query_results['matches']]

    return context_chunks

def delete_index(index_name: str) -> None:
    """
    Delete a specified index from Pinecone.

    Args:
        index_name (str): The name of the index to be deleted.
    """
    if index_name in pc.list_indexes().names():
        print("\nDeleting index ...")
        pc.delete_index(name=index_name)
        print(f"Index {index_name} deleted successfully")
    else:
        print("\nNo index to delete!")
