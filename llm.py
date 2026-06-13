import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# FIX: Initialize the client correctly using genai.Client
# Note: If your key is named exactly GOOGLE_API_KEY or GEMINI_API_KEY in your .env,
# you can just call genai.Client() empty and it will auto-detect it.
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def query_llm_with_content(query: str, context: str) -> str:
    
    system_instruction = (
        "You are a helpful, professional assistant. Answer the user's question "
        "using ONLY the provided reference context. If the answer cannot be found "
        "in the context, politely state that you do not know."
    )
    
    # FIX: Combine the context and the user query together 
    # so the model has the information required to follow the instructions.
    full_prompt = f"""
    Reference Context:
    {context}
    
    User Question: {query}
    
    Answer:
    """
    
    # Send the bundled string to gemini-2.5-flash
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt,  # Pass the combined text here
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.3,
        )
    )
    
    return response.text