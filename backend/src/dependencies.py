from src.application.ingest_use_case import IngestDocumentUseCase
from src.application.chat_use_case import ChatUseCase

# Global variables for dependencies
ingest_use_case: IngestDocumentUseCase = None
chat_use_case: ChatUseCase = None


def get_ingest_use_case() -> IngestDocumentUseCase:
    if not ingest_use_case:
        raise RuntimeError("Ingest use case not initialized")
    return ingest_use_case


def get_chat_use_case() -> ChatUseCase:
    if not chat_use_case:
        raise RuntimeError("Chat use case not initialized")
    return chat_use_case
