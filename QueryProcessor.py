from embedder import embed_User_query
from llm import query_llm_with_content
from vectorstore import search_pinecone

def process_query(user_query: str):
    # Step 1: Embed the user query
    query_embedding = embed_User_query(user_query)
    
    # Step 2: Search Pinecone with the query embedding
    retrieved_chunks = search_pinecone(query_embedding, top_k=4, namespace="")
    
    querry_llm_response = query_llm_with_content(user_query, " ".join(retrieved_chunks))
    print(f"LLM Response: {querry_llm_response}")
    
    #return retrieved_chunks
    
if __name__ == "__main__":
    user_query = "What is the company's policy on working hours?"
    results = process_query(user_query)
    