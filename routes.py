from fastapi import APIRouter, HTTPException

from .schemas import (
    DocumentRequest,
    DocumentResponse
)

from .services.document_service import generate_document


router = APIRouter()


@router.post(
    "/generate",
    response_model=DocumentResponse
)
def generate(request: DocumentRequest):

    try:

        content, model = generate_document(
            request.model_dump()
        )

        return DocumentResponse(
            document_type=request.document_type,
            content=content,
            model=model
        )

    except RuntimeError as exc:

        raise HTTPException(
            status_code=503,
            detail=str(exc)
        )

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=f"Document generation failed: {exc}"
        )