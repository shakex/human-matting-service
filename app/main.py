import os
import sys
import json
import uvicorn
from fastapi import FastAPI, Depends
from loguru import logger
import asyncio

LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(LOCAL_PATH, '..'))

from app.service.matting_service import MattingService, get_matting_service
from app.model.request.matting_req import MattingRequest, BgReplaceRequest
from app.model.response.matting_resp import MattingResponse

app = FastAPI(
    title='Human Matting Service API Document',
    description='人脸抠像服务接口文档',
    version='1.0.0'
)


@app.post('/human-matting', response_model=MattingResponse, name="人像抠图")
async def human_matting(request: MattingRequest, service: MattingService = Depends(get_matting_service)):
    logger.info('开始人像抠图模型进行推理')
    loop = asyncio.get_event_loop()
    resp = await loop.run_in_executor(None,
                                      service.human_matting,
                                      request.img,
                                      request.max_width)
    return resp


@app.post('/replace-background', response_model=MattingResponse, name="背景替换")
async def replace_background(request: BgReplaceRequest, service: MattingService = Depends(get_matting_service)):
    logger.info('开始人像抠图并替换背景')
    loop = asyncio.get_event_loop()
    resp = await loop.run_in_executor(None,
                                      service.replace_background,
                                      request.img,
                                      request.max_width,
                                      request.max_height,
                                      request.color)
    return resp


if __name__ == '__main__':
    config = '../config.json'
    with open(config) as json_file:
        cfg = json.load(json_file)
    uvicorn.run(app='main:app',
                host=cfg['host'],
                port=cfg['port'],
                reload=cfg['reload'],
                debug=cfg['debug'],
                workers=cfg['workers'])
