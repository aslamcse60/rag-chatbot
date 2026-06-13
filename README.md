# RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that processes PDF documents and answers user queries using context-aware responses powered by Google's Gemini LLM.

## Project Overview

This project implements a RAG pipeline that:

1. **Extracts** text from PDF documents
2. **Chunks** the text into manageable pieces
3. **Embeds** chunks using Google's embedding model
4. **Stores** embeddings in Pinecone vector database
5. **Retrieves** relevant chunks based on user queries
6. **Generates** accurate answers using Google Gemini LLM with retrieved context

## Architecture

```
PDF Document
    ↓
PDFReader (extract text)
    ↓
Chunker (split into overlapping chunks)
    ↓
Embedder (create vector embeddings)
    ↓
Pinecone Vector Store (store & index)
    ↓
QueryProcessor (search → retrieve → generate answer)
    ↓
Google Gemini LLM (generate contextual response)
```

## Project Structure

```
rag-chatbot/
├── pdfreader.py          # PDF text extraction
├── chunker.py            # Text chunking with overlap
├── embedder.py           # Text embedding using Gemini
├── vectorstore.py        # Pinecone integration
├── dataprocessor.py      # Main data ingestion pipeline
├── llm.py                # Gemini LLM query handler
├── QueryProcessor.py     # Query processing pipeline
├── requirements.txt      # Python dependencies
├── resources/
│   └── HR_Policy.pdf     # Sample PDF document
└── README.md             # This file
```

## Prerequisites

- Python 3.8+
- Google API Key (for Gemini and embeddings)
- Pinecone API Key and Index
- pip (Python package manager)

## Setup Instructions

### Step 1: Clone the Repository

```bash
cd d:\Dev\rag-chatbot
```

### Step 2: Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies:**

- `pypdf` - PDF reading and text extraction
- `google-generativeai` - Google Gemini LLM and embeddings
- `pinecone-client` - Vector database operations
- `python-dotenv` - Environment variable management

### Step 4: Configure Environment Variables

Create a `.env` file in the project root directory:

```env
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=your_pinecone_index_name
```

#### Getting API Keys:

**Google API Key:**

- Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
- Create or copy your API key
- This key works for both Gemini and Embeddings API

**Pinecone API Key:**

- Sign up at [Pinecone](https://www.pinecone.io/)
- Create a project and index
- Copy your API key from the dashboard
- Note your index name

### Step 5: Add Your PDF Documents

1. Place your PDF files in the `resources/` folder
2. Update the `pdf_path` in `dataprocessor.py` if using a different filename:
   ```python
   pdf_path = "./resources/your_document.pdf"
   ```

## Usage

### Step 1: Process and Index PDF Documents

Run the data processor to extract, chunk, and embed your PDFs:

```bash
python dataprocessor.py
```

This will:

1. Read the PDF from `resources/` folder
2. Split text into chunks (default: 900 characters with 150 character overlap)
3. Generate embeddings using Gemini
4. Store vectors in Pinecone

**Expected Output:**

```
Successfully processed and stored embeddings in Pinecone
```

### Step 2: Query the Chatbot

Run the query processor to ask questions:

```bash
python QueryProcessor.py
```

Modify the `user_query` variable in `QueryProcessor.py` to ask different questions:

```python
if __name__ == "__main__":
    user_query = "What is the company's policy on working hours?"
    results = process_query(user_query)
```

**Expected Output:**

```
Found X matches in Query.
LLM Response: [Your answer based on the PDF content]
```

## File Descriptions

### `pdfreader.py`

Extracts text from PDF files using PyPDF library.

- **Function:** `extract_text_from_pdf(pdf_path)` → List of page texts

### `chunker.py`

Splits extracted text into overlapping chunks for better semantic coverage.

- **Function:** `chunk_pages(pages, chunk_size=900, chunk_overlap=150)` → List of text chunks
- **Default:** 900 character chunks with 150 character overlap

### `embedder.py`

Converts text into vector embeddings using Google's Gemini Embedding model.

- **Function:** `embed_chunks(chunks)` → List of embedding vectors
- **Function:** `embed_User_query(user_query)` → Single embedding vector
- **Model:** `gemini-embedding-2`

### `vectorstore.py`

Manages Pinecone vector database operations (storage and retrieval).

- **Function:** `store_in_pinecone(chunks, embeddings, namespace)` → Stores vectors
- **Function:** `search_pinecone(query_embedding, top_k, namespace)` → Retrieves top-k chunks

### `llm.py`

Handles LLM interactions using Google Gemini with retrieved context.

- **Function:** `query_llm_with_content(query, context)` → Generated response
- **Model:** `gemini-2.5-flash`
- **Temperature:** 0.3 (for deterministic answers)

### `dataprocessor.py`

Main pipeline orchestrating the entire ingestion process.

- **Function:** `run()` → Executes full pipeline

### `QueryProcessor.py`

Handles user query processing with retrieval and generation.

- **Function:** `process_query(user_query)` → Processes query and returns LLM response
- **Top-K:** Retrieves top 4 most relevant chunks

## Customization

### Adjust Chunking Parameters

In `dataprocessor.py`:

```python
chunks = chunk_pages(pages, chunk_size=1200, chunk_overlap=200)
```

### Change Number of Retrieved Chunks

In `QueryProcessor.py`:

```python
retrieved_chunks = search_pinecone(query_embedding, top_k=10, namespace="")
```

### Modify LLM Temperature

In `llm.py`:

```python
config=types.GenerateContentConfig(
    system_instruction=system_instruction,
    temperature=0.7,  # Increase for more creative responses
)
```

## Troubleshooting

| Issue                  | Solution                                                |
| ---------------------- | ------------------------------------------------------- |
| `API Key not found`    | Verify `.env` file exists and keys are correct          |
| `PDF file not found`   | Check file path in `dataprocessor.py`                   |
| `Pinecone Index error` | Verify index name and API key in `.env`                 |
| `No matches found`     | Ensure data was processed with `dataprocessor.py` first |
| `Rate limit errors`    | Add delays between API calls or upgrade API quota       |

## Performance Notes

- **Embedding Time:** ~1-2 seconds per 1000 tokens
- **Query Retrieval:** ~100-500ms
- **LLM Response:** ~2-5 seconds
- **Vector Storage:** Scales efficiently to millions of chunks

## Future Enhancements

- [ ] Support for multiple document formats (DOCX, TXT, MD)
- [ ] Web UI for interactive querying
- [ ] Batch processing for large document collections
- [ ] Custom system prompts and response templates
- [ ] Citation tracking for retrieved sources
- [ ] Document versioning and update management

## Support

For issues or questions, please refer to:

- [Google Generative AI Docs](https://ai.google.dev/)
- [Pinecone Documentation](https://docs.pinecone.io/)
