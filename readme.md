# Simple RAG agent
A Retrieval-Augmented Generation (RAG) agent built with LangChain, Streamlit, and vector databases. This app allows users to upload documents (PDFs, etc.), which are indexed into a vector store. The agent can then answer questions by retrieving relevant chunks from the uploaded documents and generating human-friendly responses.

## Features
- Upload PDFs and automatically index them into a vector store.

- Embeddings generated using HuggingFace models (local or hosted).

- Retrieve relevant chunks from documents for question answering.

- Chat interface powered by LangChain.

- Persistent vector database (FAISS/Chroma).

- Environment variable support for API keys.


##  Models Used
###  LLM
- **Google Generative ai**: gemini-2.5-flash.

### Embedding models
- **Cohere Embeddings (hosted,limited)**: embed-english-v3.0.
- **Hugging Face Embeddings (local,free)**: all-MiniLM-L12-v2.

### Vector Databases
- **Default**: Chroma.
- **Optional**: FAISS.
