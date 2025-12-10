import os
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from src.domain.interfaces import LLMService, EmbeddingService
from src.domain.entities import Chunk, ChatMessage


class GeminiService(LLMService):
    """
    Implementation of LLMService using Google's Gemini model via LangChain.
    """

    def __init__(self, api_key: str = None, model: str = "gemini-pro"):
        """
        Initialize the Gemini service.

        Args:
            api_key: Google API key. If None, looks for GOOGLE_API_KEY env var.
            model: The model name to use (default: gemini-pro).
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Google API key must be provided or set in "
                "GOOGLE_API_KEY environment variable."
            )

        self.llm = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=self.api_key,
            convert_system_message_to_human=True,
        )

    async def generate_response(
        self, query: str, context: List[Chunk], history: List[ChatMessage]
    ) -> str:
        """
        Generates a response from the LLM based on query, context, and history.
        """
        # Construct context string
        context_str = "\n\n".join([c.text for c in context])

        # System prompt
        system_prompt = (
            "You are a helpful assistant. Use the following context to answer "
            "the user's question.\n"
            "If the answer is not in the context, say you don't know.\n\n"
            f"Context:\n{context_str}\n"
        )

        messages = [SystemMessage(content=system_prompt)]

        # Add history
        for msg in history:
            if msg.role == "user":
                messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                messages.append(AIMessage(content=msg.content))
            elif msg.role == "system":
                # System messages in history are usually not supported well
                # in chat history reconstruction for some models, but we can
                # add them if needed. For now, we'll skip or treat as system.
                pass

        # Add current query
        messages.append(HumanMessage(content=query))

        response = await self.llm.ainvoke(messages)
        return str(response.content)


class GeminiEmbeddingService(EmbeddingService):
    """
    Implementation of EmbeddingService using Google's Gemini embeddings.
    """

    def __init__(self, api_key: str = None, model: str = "models/embedding-001"):
        """
        Initialize the Gemini embedding service.

        Args:
            api_key: Google API key. If None, looks for GOOGLE_API_KEY env var.
            model: The model name to use (default: models/embedding-001).
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Google API key must be provided or set in "
                "GOOGLE_API_KEY environment variable."
            )

        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=model,
            google_api_key=self.api_key,
        )

    async def embed_text(self, text: str) -> List[float]:
        """Generates an embedding for a single text string."""
        return await self.embeddings.aembed_query(text)

    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generates embeddings for a list of text strings."""
        return await self.embeddings.aembed_documents(texts)
