RAG Production — Document Q&A System
=====================================

A production-style Retrieval-Augmented Generation (RAG) pipeline that
answers questions over PDF documents, built with industry-standard tools.


STACK
-----
- Orchestration: LangChain (LCEL)
- Vector DB: Qdrant
- Embeddings: sentence-transformers (all-MiniLM-L6-v2)
- LLM: Ollama (local, llama3.2:3b)
- API: FastAPI
- Testing: pytest
- Containerization: Docker + docker-compose


ARCHITECTURE
------------
PDF documents -> Document Loader -> Text Splitter -> Embeddings -> Qdrant
                                                                      |
User question -> Retriever (top-k) -> Prompt + Context -> Ollama LLM -> Answer + Sources


PROJECT STRUCTURE
------------------
rag_production/
    app/
        api.py          - FastAPI endpoints
        chain.py         - Retrieval + generation pipeline (LCEL)
        config.py         - Central configuration
        ingest.py          - Document loading, chunking, indexing
    evaluation/
        evaluate.py         - Keyword-based answer evaluation
    tests/
        test_chunking.py
        test_retrieval.py
        test_api.py
    data/                     - Source PDF documents
    Dockerfile
    docker-compose.yml
    requirements.txt


SETUP
-----
1. Clone the repo and install dependencies:
   pip install -r requirements.txt

2. Pull the local model with Ollama (https://ollama.com):
   ollama pull llama3.2:3b

3. Start Qdrant:
   docker run -p 6333:6333 -v ./qdrant_storage:/qdrant/storage qdrant/qdrant

4. Add PDF files to data/, then index them:
   python -m app.ingest

5. Run the API:
   uvicorn app.api:app --reload

6. Open http://localhost:8000/docs to test the /query endpoint.


OR RUN EVERYTHING WITH DOCKER
------------------------------
docker-compose up --build

(Requires Ollama running on the host machine.)


EXAMPLE
-------
Request:
  POST /query
  { "question": "What data types exist in MongoDB?" }

Response:
  {
    "answer": "Integer, String, Date, Binary, Array, and Object.",
    "sources": [
      { "source": "data/aula2-BDII.pdf", "page": 4 }
    ]
  }


TESTING
-------
pytest tests/ -v


EVALUATION
----------
A lightweight keyword-based evaluation script checks answer quality
against a small test set:

  python -m evaluation.evaluate


NEXT STEPS
----------
- Integrate RAGAS (https://github.com/explodinggradients/ragas) for
  faithfulness and relevancy scoring
- Add observability with Langfuse (trace latency, token usage, cost
  per query)
- CI/CD with GitHub Actions running tests on every push
- Swap Ollama for a hosted LLM API for production deployment


WHY THIS PROJECT
-----------------
Built to demonstrate an end-to-end RAG pipeline using the tools
commonly used in production systems, evolving from a from-scratch
implementation (manual chunking, cosine similarity, and embedding
storage) into a LangChain + Qdrant-based architecture.