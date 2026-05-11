import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from src.core.config import Settings


class VectorStoreService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key or None)

    def ensure_collection(self, collection_name: str | None = None) -> str:
        name = collection_name or self.settings.qdrant_collection
        existing = [collection.name for collection in self.client.get_collections().collections]
        if name not in existing:
            self.client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(
                    size=self.settings.embedding_dimension,
                    distance=Distance.COSINE,
                ),
            )
        return name

    def upsert_documents(
        self,
        vectors: list[list[float]],
        payloads: list[dict],
        collection_name: str | None = None,
    ) -> int:
        name = self.ensure_collection(collection_name)
        points = []

        for vector, payload in zip(vectors, payloads):
            raw_id = f"{payload.get('source')}:{payload.get('chunk_index')}:{payload.get('text', '')[:80]}"
            point_id = str(uuid.uuid5(uuid.NAMESPACE_URL, raw_id))
            points.append(PointStruct(id=point_id, vector=vector, payload=payload))

        self.client.upsert(collection_name=name, points=points)
        return len(points)

    def search(self, query_vector: list[float], collection_name: str | None = None, top_k: int = 4):
        name = self.ensure_collection(collection_name)
        return self.client.search(
            collection_name=name,
            query_vector=query_vector,
            limit=top_k,
            with_payload=True,
        )

    def describe_collection(self, collection_name: str | None = None) -> dict:
        name = self.ensure_collection(collection_name)
        info = self.client.get_collection(name)
        return {"name": name, "vectors_count": info.vectors_count, "status": str(info.status)}
