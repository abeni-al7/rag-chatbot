from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import weaviate
from src.infrastructure.gemini_service import (
    GeminiService,
    GeminiEmbeddingService,
)
from src.infrastructure.pdf_parser import PDFParser
from src.infrastructure.weaviate_repo import WeaviateRepository
from src.application.ingest_use_case import IngestDocumentUseCase
from src.application.chat_use_case import ChatUseCase
from src import dependencies
from src.interfaces.api import router as api_router

# Global variables for dependencies
weaviate_client = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global weaviate_client

    # Initialize Weaviate Client
    # Connect to local Weaviate instance
    # (assumes running via docker-compose on port 8080)
    weaviate_client = weaviate.use_async_with_local()
    await weaviate_client.connect()

    # Initialize Infrastructure
    # Note: Ensure GOOGLE_API_KEY is set in environment variables
    gemini_service = GeminiService()
    embedding_service = GeminiEmbeddingService()
    pdf_parser = PDFParser()
    weaviate_repo = WeaviateRepository(client=weaviate_client)

    # Ensure Weaviate collection exists
    # Accessing protected method for initialization
    await weaviate_repo._ensure_collection()

    # Initialize Use Cases
    dependencies.ingest_use_case = IngestDocumentUseCase(
        parser=pdf_parser,
        repo=weaviate_repo,
        embedding_service=embedding_service,
    )

    dependencies.chat_use_case = ChatUseCase(
        repo=weaviate_repo,
        llm_service=gemini_service,
        embedding_service=embedding_service,
    )

    yield

    # Cleanup
    if weaviate_client:
        await weaviate_client.close()


app = FastAPI(title="RAG Chatbot API", lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "RAG Chatbot API is running"}
