#  Here we load a document into a chroma db
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
    
def build_retriever():
    db = Chroma(persist_directory="./app/facts_db", embedding_function=OpenAIEmbeddings())
    return db.as_retriever()

