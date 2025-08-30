import streamlit as st
import tempfile

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# embeddings = CohereEmbeddings(model="embed-english-v3.0", cohere_api_key="YOUR_KEY")
@st.cache_resource
def get_embedding():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L12-v2")

@st.cache_resource
def get_vectorstore():
    return Chroma(persist_directory="./chroma_db", embedding_function=get_embedding())


def add_pdf(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file.getbuffer())
        file_path = tmp.name

    loader = PyPDFLoader(file_path)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1020, chunk_overlap=128)
    docs = splitter.split_documents(documents)
    vs = get_vectorstore()
    vs.add_documents(docs)
    return vs


# @st.cache_resource
# def create_index_from_file(file_name):
#     loaders = [PyPDFLoader(file_name)]
#     index = VectorstoreIndexCreator(
#         embedding=embedding,
#         text_splitter=RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
#     ).from_loaders(loaders)

#     return index

if __name__ == "__main__":
    print("ingest")
