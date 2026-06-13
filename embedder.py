from google import genai
from dotenv import load_dotenv
import os
from typing import List

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
EMBEDDING_MODEL = "gemini-embedding-2" # Updated to the latest embedding model

def embed_chunks(chunks: List[str]) -> List[List[float]]:
    """
    Embed the text chunks using Google's embedding model.
    
    Args:
        chunks (List[str]): List of text chunks to embed.
        
    Returns:
        List[List[float]]: List of embedding vectors for each chunk.
    """
    embeddings = []
    
    for chunk in chunks:
        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=chunk  # Changed from input=chunk
        )
        # Changed from response.data[0].embedding
        embedding_vector = response.embeddings[0].values
        embeddings.append(embedding_vector)
    
    #print(f"Embedded 2:", embeddings[:2])  # Print the first 2 embeddings for verification")
    return embeddings

def embed_User_query(user_query: str) -> List[float]:
    """
    Embed the user query using Google's embedding model.
    
    Args:
        user_query (str): The user's query to embed.
        
    Returns:
        List[float]: The embedding vector for the user query.
    """
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=user_query  # Changed from input=user_query
    )
    # Changed from response.data[0].embedding
    query_embedding = response.embeddings[0].values
    
    #print(f"Embedded User Query:", query_embedding)  # Print the embedding for verification
    return query_embedding