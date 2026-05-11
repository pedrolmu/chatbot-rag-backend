from src.utils.chunking import chunk_text


def test_chunk_text_generates_metadata():
    text = "abc " * 400
    chunks = chunk_text(text, source="teste.txt", max_size=100, overlap=20)
    assert len(chunks) > 1
    assert chunks[0].metadata["source"] == "teste.txt"
    assert chunks[0].metadata["chunk_index"] == 0
