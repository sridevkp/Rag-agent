import streamlit as st
import tempfile
import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_cohere import CohereEmbeddings
from langchain.indexes import VectorstoreIndexCreator

@st.cache_resource
def get_splitter():
    return RecursiveCharacterTextSplitter(chunk_size=1020, chunk_overlap=128)

@st.cache_resource
def get_embedding():
    return CohereEmbeddings(model="embed-english-v3.0", cohere_api_key=os.getenv("COHERE_API_KEY"))


def load_file(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.name)[1]) as tmp:
        tmp.write(file.getbuffer())
        file_path = tmp.name

    if file.name.endswith(".pdf"):
        return PyPDFLoader(file_path)
    elif file.name.endswith(".txt"):
        return TextLoader(file_path, encoding="utf-8")
    else:
        st.warning(f"⚠️ Unsupported file type: {file.name}")
        return None

def add_file(index, file):
    loader = load_file(file)
    docs = loader.load()
    splits = get_splitter().split_documents(docs)
    st.session_state.index.vectorstore.add_documents(splits)


def create_index_from_file(file):
    loaders = load_file(file)
    index = VectorstoreIndexCreator(
        embedding=get_embedding(),
        text_splitter=get_splitter()  
    ).from_loaders([loaders])
    return index



if __name__ == "__main__":
    print("ingest")
