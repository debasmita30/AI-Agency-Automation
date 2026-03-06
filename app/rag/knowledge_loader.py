from langchain.document_loaders import TextLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DOC_PATH = os.path.join(BASE_DIR, "agency_docs.txt")

loader = TextLoader(DOC_PATH)

documents = loader.load()

embeddings = HuggingFaceEmbeddings()

vector_store = FAISS.from_documents(
    documents,
    embeddings
)

def retrieve_context(query):

    docs = vector_store.similarity_search(query, k=2)

    context = " ".join([doc.page_content for doc in docs])

    return context