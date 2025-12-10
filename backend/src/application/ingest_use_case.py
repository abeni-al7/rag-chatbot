from typing import Any, List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.domain.entities import Chunk
from src.domain.interfaces import (
    DocumentParser,
    VectorStoreRepository,
    EmbeddingService,
)


class IngestDocumentUseCase:
    """
    Use case for ingesting documents into the system.
    """

    def __init__(
        self,
        parser: DocumentParser,
        repo: VectorStoreRepository,
        embedding_service: EmbeddingService,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        self.parser = parser
        self.repo = repo
        self.embedding_service = embedding_service
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    async def execute(self, file_source: Any, source_name: str = "unknown") -> None:
        """
        Executes the ingestion process: Parse -> Chunk -> Embed -> Store.

        Args:
            file_source: The file content or path to be parsed.
            source_name: The name of the source (e.g., filename).
        """
        # 1. Parse the document
        documents = await self.parser.parse(file_source)

        chunks_to_store: List[Chunk] = []

        for doc in documents:
            # 2. Chunk the content
            # We use langchain's splitter which works on text
            split_texts = self.text_splitter.split_text(doc.content)

            # 3. Generate embeddings
            embeddings = await self.embedding_service.embed_documents(split_texts)

            # 4. Create Chunk entities
            for i, text in enumerate(split_texts):
                chunk = Chunk(
                    text=text,
                    embedding=embeddings[i],
                    metadata={
                        **doc.metadata,
                        "source": source_name,
                        "chunk_index": i,
                    },
                )
                chunks_to_store.append(chunk)

        # 5. Store in Vector DB
        if chunks_to_store:
            await self.repo.add_chunks(chunks_to_store)
