import pytest
from unittest.mock import Mock, AsyncMock
from src.application.chat_use_case import ChatUseCase
from src.domain.entities import ChatMessage, Chunk, Citation
from src.domain.interfaces import (
    VectorStoreRepository,
    LLMService,
    EmbeddingService,
)


@pytest.fixture
def mock_repo():
    return Mock(spec=VectorStoreRepository)


@pytest.fixture
def mock_llm_service():
    return Mock(spec=LLMService)


@pytest.fixture
def mock_embedding_service():
    return Mock(spec=EmbeddingService)


@pytest.fixture
def chat_use_case(mock_repo, mock_llm_service, mock_embedding_service):
    return ChatUseCase(
        repo=mock_repo,
        llm_service=mock_llm_service,
        embedding_service=mock_embedding_service,
    )


@pytest.mark.asyncio
async def test_chat_execute_success(
    chat_use_case, mock_repo, mock_llm_service, mock_embedding_service
):
    # Setup mocks
    query = "What is RAG?"
    history = [ChatMessage(role="user", content="Hello")]

    # Mock embedding
    mock_embedding_service.embed_text = AsyncMock(return_value=[0.1, 0.2, 0.3])

    # Mock retrieval
    mock_chunks = [
        Chunk(
            text="RAG stands for Retrieval-Augmented Generation.",
            metadata={"source": "doc1.pdf", "page_number": 1},
        ),
        Chunk(
            text="It combines retrieval with generation.",
            metadata={"source": "doc1.pdf", "page_number": 1},  # Duplicate source/page
        ),
        Chunk(text="Another fact.", metadata={"source": "doc2.pdf", "page_number": 5}),
    ]
    mock_repo.search = AsyncMock(return_value=mock_chunks)

    # Mock LLM generation
    mock_llm_service.generate_response = AsyncMock(
        return_value="RAG is Retrieval-Augmented Generation."
    )

    # Execute
    response = await chat_use_case.execute(query, history)

    # Verify
    mock_embedding_service.embed_text.assert_called_once_with(query)
    mock_repo.search.assert_called_once()
    mock_llm_service.generate_response.assert_called_once_with(
        query, mock_chunks, history
    )

    assert response.answer == "RAG is Retrieval-Augmented Generation."

    # Verify citations (should be unique by source+page)
    assert len(response.citations) == 2

    # Check first citation
    assert response.citations[0].source == "doc1.pdf"
    assert response.citations[0].page_number == 1

    # Check second citation
    assert response.citations[1].source == "doc2.pdf"
    assert response.citations[1].page_number == 5
