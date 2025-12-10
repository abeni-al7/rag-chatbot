from abc import ABC, abstractmethod
from typing import List, Any
from src.domain.entities import Document, Chunk, ChatMessage


class VectorStoreRepository(ABC):
    """Interface for vector store operations."""

    @abstractmethod
    async def add_chunks(self, chunks: List[Chunk]) -> None:
        """Adds chunks to the vector store."""
        pass

    @abstractmethod
    async def search(self, query_vector: List[float], limit: int = 5) -> List[Chunk]:
        """Searches for relevant chunks based on a query vector."""
        pass


class LLMService(ABC):
    """Interface for Large Language Model services."""

    @abstractmethod
    async def generate_response(
        self, query: str, context: List[Chunk], history: List[ChatMessage]
    ) -> str:
        """
        Generates a response from the LLM based on query, context, and history.
        """
        pass


class DocumentParser(ABC):
    """Interface for document parsing."""

    @abstractmethod
    async def parse(self, file_source: Any) -> List[Document]:
        """Parses a file source into a list of Documents."""
        pass


class EmbeddingService(ABC):
    """Interface for embedding generation."""

    @abstractmethod
    async def embed_text(self, text: str) -> List[float]:
        """Generates an embedding for a single text string."""
        pass

    @abstractmethod
    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generates embeddings for a list of text strings."""
        pass
