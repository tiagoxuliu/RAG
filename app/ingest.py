from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

from app.config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    QDRANT_URL,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
)

def ingest_documents():
    loader = DirectoryLoader("data", glob="**/*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    print("numbers of documents created:", len(documents))
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    texts = text_splitter.split_documents(documents)
    print("numbers of documents after split:", len(texts))
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    QdrantVectorStore.from_documents(
        documents=texts,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        url=QDRANT_URL,
    )
    print("numbers of chunks added to Qdrant:", len(texts))


if __name__ == "__main__":
    ingest_documents()