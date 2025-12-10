import pytest
from unittest.mock import Mock, AsyncMock
from src.application.ingest_use_case import IngestDocumentUseCase
from src.domain.entities import Document, Chunk
from src.domain.interfaces import (
    DocumentParser,
    VectorStoreRepository,
    EmbeddingService,
)


@pytest.fixture
def mock_parser():
    return Mock(spec=DocumentParser)


@pytest.fixture
def mock_repo():
    return Mock(spec=VectorStoreRepository)


@pytest.fixture
def mock_embedding_service():
    return Mock(spec=EmbeddingService)


@pytest.fixture
def ingest_use_case(mock_parser, mock_repo, mock_embedding_service):
    return IngestDocumentUseCase(
        parser=mock_parser,
        repo=mock_repo,
        embedding_service=mock_embedding_service,
        chunk_size=100,
        chunk_overlap=10,
    )


@pytest.mark.asyncio
async def test_ingest_document_success(
    ingest_use_case, mock_parser, mock_repo, mock_embedding_service
):
    # Setup mocks
    mock_file = b"fake pdf content"
    mock_documents = [
        Document(content="This is page 1 content.", metadata={"page_number": 1}),
        Document(content="This is page 2 content.", metadata={"page_number": 2}),
    ]
    mock_parser.parse = AsyncMock(return_value=mock_documents)

    # Mock embeddings: return list of floats for each text chunk
    # Assuming text splitter doesn't split these short strings further
    mock_embedding_service.embed_documents = AsyncMock(
        return_value=[
            [0.1, 0.2],  # Embedding for page 1
            [0.3, 0.4],  # Embedding for page 2
        ]
    )

    mock_repo.add_chunks = AsyncMock()

    # Execute
    await ingest_use_case.execute(mock_file, source_name="test.pdf")

    # Verify
    mock_parser.parse.assert_called_once_with(mock_file)

    # Verify embeddings were generated
    assert (
        mock_embedding_service.embed_documents.call_count == 2
    )  # Once per document loop

    # Verify chunks were added to repo
    mock_repo.add_chunks.assert_called_once()
    call_args = mock_repo.add_chunks.call_args[0][0]
    assert len(call_args) == 2
    assert isinstance(call_args[0], Chunk)
    assert call_args[0].text == "This is page 1 content."
    assert call_args[0].metadata["source"] == "test.pdf"
    assert call_args[0].metadata["page_number"] == 1
    assert call_args[1].text == "This is page 2 content."
