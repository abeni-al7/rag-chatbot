from typing import List
from dataclasses import dataclass
from src.domain.entities import ChatMessage, Citation, Chunk
from src.domain.interfaces import (
    VectorStoreRepository,
    LLMService,
    EmbeddingService,
)


@dataclass
class ChatResponse:
    answer: str
    citations: List[Citation]


class ChatUseCase:
    """
    Use case for chatting with the RAG system.
    """

    def __init__(
        self,
        repo: VectorStoreRepository,
        llm_service: LLMService,
        embedding_service: EmbeddingService,
    ):
        self.repo = repo
        self.llm_service = llm_service
        self.embedding_service = embedding_service

    async def execute(
        self, query: str, history: List[ChatMessage]
    ) -> ChatResponse:
        """
        Executes the chat process: Embed -> Retrieve -> Generate.

        Args:
            query: The user's question.
            history: The chat history.

        Returns:
            ChatResponse containing the answer and citations.
        """
        # 1. Embed the query
        query_embedding = await self.embedding_service.embed_text(query)

        # 2. Retrieve relevant chunks
        relevant_chunks = await self.repo.search(query_embedding, limit=5)

        # 3. Generate answer
        answer = await self.llm_service.generate_response(
            query, relevant_chunks, history
        )

        # 4. Extract citations
        citations = self._extract_citations(relevant_chunks)

        return ChatResponse(answer=answer, citations=citations)

    def _extract_citations(self, chunks: List[Chunk]) -> List[Citation]:
        """
        Extracts unique citations from chunks.
        """
        seen = set()
        citations = []
        for chunk in chunks:
            source = chunk.metadata.get("source", "unknown")
            page_number = chunk.metadata.get("page_number", 0)
            
            # Create a tuple for hashing/uniqueness check
            citation_key = (source, page_number)
            
            if citation_key not in seen:
                seen.add(citation_key)
                citations.append(
                    Citation(source=source, page_number=page_number)
                )
        
        return citations
