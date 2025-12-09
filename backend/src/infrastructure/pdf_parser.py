import io
from typing import List, Union
from pypdf import PdfReader
from src.domain.interfaces import DocumentParser
from src.domain.entities import Document


class PDFParser(DocumentParser):
    """
    Implementation of DocumentParser for PDF files using pypdf.
    """

    async def parse(self, file_source: Union[bytes, io.BytesIO]) -> List[Document]:
        """
        Parses a PDF file source into a list of Documents (one per page).

        Args:
            file_source: The PDF content as bytes or a file-like object.

        Returns:
            List[Document]: A list of documents, where each document
            represents a page.
        """
        if isinstance(file_source, bytes):
            stream = io.BytesIO(file_source)
        else:
            stream = file_source

        reader = PdfReader(stream)
        documents = []

        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                documents.append(
                    Document(content=text, metadata={"page_number": i + 1})
                )

        return documents
