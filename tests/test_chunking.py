from langchain_text_splitters import RecursiveCharacterTextSplitter

TEXTO_TESTE = (
    "Bases de Dados II trata de modelação em MongoDB e SGBD relacionais. " * 10
)

def test_chunk_respects_size():
    splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=10)
    chunks = splitter.split_text(TEXTO_TESTE)
    assert all(len(chunk) <= 100 for chunk in chunks)

def test_chunk_not_empty():
    splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=10)
    chunks = splitter.split_text(TEXTO_TESTE)
    assert all(chunk.strip() != "" for chunk in chunks)
    assert len(chunks) > 0

def test_chunk_overlap_creates_more_chunks_than_no_overlap():
    with_overlap = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=50)
    without_overlap = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    assert len(with_overlap.split_text(TEXTO_TESTE)) >= len(without_overlap.split_text(TEXTO_TESTE))