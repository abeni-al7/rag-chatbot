import weaviate
import weaviate.classes.config as wvc
import weaviate.classes.query as wvq
from weaviate.classes.data import DataObject
from typing import List
from src.domain.interfaces import VectorStoreRepository
from src.domain.entities import Chunk


class WeaviateRepository(VectorStoreRepository):
    def __init__(self, client: weaviate.WeaviateAsyncClient):
        self.client = client
        self.collection_name = "Chunk"

    async def _ensure_collection(self):
        exists = await self.client.collections.exists(self.collection_name)
        if not exists:
            await self.client.collections.create(
                name=self.collection_name,
                vectorizer_config=wvc.Configure.Vectorizer.none(),
                properties=[
                    wvc.Property(name="text", data_type=wvc.DataType.TEXT),
                    wvc.Property(name="source", data_type=wvc.DataType.TEXT),
                    wvc.Property(name="page_number", data_type=wvc.DataType.INT),
                ],
            )

    async def add_chunks(self, chunks: List[Chunk]) -> None:
        await self._ensure_collection()
        collection = self.client.collections.get(self.collection_name)

        data_objects = []
        for chunk in chunks:
            if chunk.embedding is None:
                continue  # Skip chunks without embeddings

            props = {
                "text": chunk.text,
                "source": chunk.metadata.get("source", "unknown"),
                "page_number": chunk.metadata.get("page_number", 0),
            }
            data_objects.append(DataObject(properties=props, vector=chunk.embedding))

        if data_objects:
            await collection.data.insert_many(data_objects)

    async def search(self, query_vector: List[float], limit: int = 5) -> List[Chunk]:
        exists = await self.client.collections.exists(self.collection_name)
        if not exists:
            return []

        collection = self.client.collections.get(self.collection_name)
        response = await collection.query.near_vector(
            near_vector=query_vector,
            limit=limit,
            return_metadata=wvq.MetadataQuery(distance=True),
        )

        results = []
        for obj in response.objects:
            results.append(
                Chunk(
                    text=obj.properties.get("text", ""),
                    embedding=None,
                    metadata={
                        "source": obj.properties.get("source"),
                        "page_number": obj.properties.get("page_number"),
                        "distance": obj.metadata.distance,
                    },
                )
            )
        return results
