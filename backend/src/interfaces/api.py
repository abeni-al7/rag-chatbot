from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from src.application.ingest_use_case import IngestDocumentUseCase
from src.dependencies import get_ingest_use_case

router = APIRouter(prefix="/api")


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
        raise HTTPException(status_code=500, detail=str(e))
