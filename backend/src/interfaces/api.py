from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from pydantic import BaseModel
from src.application.ingest_use_case import IngestDocumentUseCase
from src.application.chat_use_case import ChatUseCase
from src.dependencies import get_ingest_use_case, get_chat_use_case
from src.domain.entities import ChatMessage

router = APIRouter(prefix="/api")


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    query: str
    history: List[Message] = []


class CitationModel(BaseModel):
    source: str
    page_number: int


class ChatResponseModel(BaseModel):
    answer: str
    citations: List[CitationModel]


@router.post("/ingest")
async def ingest_document(
    file: UploadFile = File(...),
    use_case: IngestDocumentUseCase = Depends(get_ingest_use_case),
):
    """
    Uploads and ingests a PDF document.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    try:
        content = await file.read()
        await use_case.execute(file_source=content, source_name=file.filename)
        return {"message": "Document ingested successfully", "filename": file.filename}
    except Exception as e:
        print(f"Ingestion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat", response_model=ChatResponseModel)
async def chat(
    request: ChatRequest,
    use_case: ChatUseCase = Depends(get_chat_use_case),
):
    """
    Answers a question based on ingested documents.
    """
    try:
        # Convert Pydantic models to domain entities
        history_entities = [
            ChatMessage(role=m.role, content=m.content) for m in request.history
        ]

        response = await use_case.execute(query=request.query, history=history_entities)

        # Convert domain response to Pydantic model
        return ChatResponseModel(
            answer=response.answer,
            citations=[
                CitationModel(source=c.source, page_number=c.page_number)
                for c in response.citations
            ],
        )
    except Exception as e:
        print(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
