from pydantic import BaseModel, Field


class MattingResponse(BaseModel):
    result: str = Field(default=None, description='结果图像（base64编码）')
