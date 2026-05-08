# services/vector_store.py

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

VECTOR_DB = {}


def create_chunks(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    return splitter.split_text(text)


def store_document(doc_id, text):

    chunks = create_chunks(text)

    vectorstore = FAISS.from_texts(
        chunks,
        embedding_model
    )

    VECTOR_DB[doc_id] = vectorstore

    return len(chunks)


def query_document(doc_id, query, k=3):

    if doc_id not in VECTOR_DB:
        return []

    docs = VECTOR_DB[doc_id].similarity_search(query, k=k)

    return [d.page_content for d in docs]