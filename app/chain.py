from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.config import (
    OLLAMA_MODEL,
    QDRANT_URL,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
)

embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
vectorstore = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name=COLLECTION_NAME,
    url=QDRANT_URL,
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
llm = OllamaLLM(model=OLLAMA_MODEL)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def answer_question(query):
    docs = retriever.invoke(query)

    context = format_docs(docs)

    prompt = ChatPromptTemplate.from_template(
        """Answer the question based only on the following context:

{context}

Question: {question}

Answer:"""
    )

    response = (
        prompt
        | llm
        | StrOutputParser()
    ).invoke({
        "context": context,
        "question": query,
    })

    return {
        "answer": response,
        "source_documents": docs,
    }


if __name__ == "__main__":
    query = "What type of data is described in the PDF?"

    result = answer_question(query)

    print("ANSWER:")
    print(result["answer"])

    print("\nSOURCE DOCUMENTS:")

    for doc in result["source_documents"]:
        print(doc)


