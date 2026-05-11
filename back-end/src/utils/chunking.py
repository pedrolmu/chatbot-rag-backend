from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    metadata: dict


def chunk_text(text: str, source: str, max_size: int = 900, overlap: int = 150) -> list[Chunk]:
    clean = " ".join(text.split())
    if not clean:
        return []

    chunks: list[Chunk] = []
    start = 0
    index = 0
    while start < len(clean):
        end = min(start + max_size, len(clean))
        piece = clean[start:end]
        chunks.append(Chunk(text=piece, metadata={"source": source, "chunk_index": index, "chars": len(piece)}))
        if end == len(clean):
            break
        start = max(0, end - overlap)
        index += 1
    return chunks
