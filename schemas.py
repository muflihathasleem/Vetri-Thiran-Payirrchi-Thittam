from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
    document_type: str = Field(min_length=1)
    parties: str = Field(min_length=1)
    terms: str = Field(min_length=1)
    effective_date: str = Field(min_length=1)
    jurisdiction: str = ""
    additional_instructions: str = ""


class DocumentResponse(BaseModel):
    document_type: str
    content: str
    model: str