from pinecone import Pinecone
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()
pinecone_client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pinecone_client.Index(os.getenv("PINECONE_INDEX_NAME"))

def store_in_pinecone(chunks, embeddings, namespace=""):
    # ... your existing Pinecone connection code ...
    
    batch = []
    
    # Loop over chunks and embeddings together
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        # Construct the exact dictionary structure Pinecone expects
        vector_record = {
            "id": f"chunk_{i}",             # Must be a string ID
            "values": embedding,            # The list of floats from Gemini
            "metadata": {"text": chunk}     # Crucial: saves the raw text to read later
        }
        batch.append(vector_record)
        
    # Now this will run cleanly without throwing a ValueError
    index.upsert(vectors=batch, namespace=namespace)
    
def search_pinecone(query_embedding, top_k: int = 4, namespace="") -> List[str]:
    # ... your existing Pinecone connection code ...
    
    # Perform the search
    search_results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        namespace=namespace
    )
    
    print(f"Found {len(search_results.matches)} matches in Query.")
    # Extract the text from metadata of search results
    retrieved_chunks = []
    for match in search_results.matches:
        if 'metadata' in match and 'text' in match.metadata:
            retrieved_chunks.append(match.metadata['text'])
    
    return retrieved_chunks