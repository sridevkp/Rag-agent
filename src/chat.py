from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv() 


def get_llm(index):
    retriever = index.vectorstore.as_retriever(search_kwargs={"k": 4})

    qa = RetrievalQA.from_chain_type(
        llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0),
        retriever=retriever,
        chain_type="map_reduce" ,
        return_source_documents=True
    )
    def llm(query):
        response = qa.invoke({"query": query})
        return response["result"]
    
    return llm

if __name__ == "__main__":
    print("This is a package file!")
