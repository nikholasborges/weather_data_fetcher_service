from pydantic import BaseModel, Field


class UploadParameter(BaseModel):
    process_id: int = Field(..., description="The process ID.")
    cities_ids: list = Field(
        ..., description="A list of city IDs to be uploaded for processing."
    )


class ProcessParameter(BaseModel):
    process_id: int = Field(..., description="The process ID.")
