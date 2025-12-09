from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


@dataclass
class Citation:
    """Represents a reference to a source document."""

    source: str
    page_number: int


@dataclass
class Chunk:
    """Represents a piece of text with its vector embedding."""

    text: str
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Document:
    """Represents an ingested document."""

    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ChatMessage:
    """Represents a message in the chat history."""

    role: str  # e.g., "user", "assistant", "system"
    content: str
