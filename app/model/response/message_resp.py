from pydantic import BaseModel

class BoundingBox(BaseModel):
    code: int
    message: int