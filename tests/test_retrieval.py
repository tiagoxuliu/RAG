from unittest.mock import MagicMock
from langchain_core.documents import Document
from app.chain import format_docs

def test_format_docs_joins_content():
    docs = [
        Document(page_content="Primeiro chunk."),
        Document(page_content="Segundo chunk."),
    ]
    resultado = format_docs(docs)
    assert "Primeiro chunk." in resultado
    assert "Segundo chunk." in resultado
    assert resultado.count("\n\n") >= 1

def test_format_docs_empty_list():
    resultado = format_docs([])
    assert resultado == ""