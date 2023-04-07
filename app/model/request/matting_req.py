from pydantic import BaseModel, Field


class MattingRequest(BaseModel):
    img: str = Field(description='图像完整路径',
                     example='')
    max_width: int = Field(default=None, description='用于识别的图像最大宽度，如图像大于预设宽度，将进行对其进行降采样处理', example=1000)


class BgReplaceRequest(BaseModel):
    img: str = Field(description='图像完整路径',
                     example='http://article.fd.zol-img.com.cn/t_s640x2000/g5/M00/01/06/ChMkJ1fNP06IEToCAAHV9-xWX6AAAVCtABzilAAAdYP527.jpg')
    max_width: int = Field(default=640, description='图片的宽度', example=640)
    max_height: int = Field(default=960, description='图片的长度', example=960)
    color: str = Field(default='#00FF00', description='替换的背景颜色，HEX格式', example='#00FF00')
