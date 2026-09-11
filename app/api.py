from fastapi import FastAPI
from pydantic import BaseModel
from app.chain import answer_question

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
def query(request: QueryRequest):
    result = answer_question(request.question)
    return {
        "answer": result["answer"],
        "sources": [
            {"source": doc.metadata.get("source"), "page": doc.metadata.get("page")}
            for doc in result["source_documents"]
        ]
    }