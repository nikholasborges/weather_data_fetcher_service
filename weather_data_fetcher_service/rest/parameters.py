from pydantic import BaseModel


class UploadParameter(BaseModel):
    process_id: int
    cities_ids: list


class ProcessParameter(BaseModel):
    process_id: int
