# -*- coding: utf-8 -*-
from fastapi import FastAPI, Depends, APIRouter
from loguru import logger
from app.service.matting_service import MattingService, get_matting_service
from app.model.request.matting_req import MattingRequest, BgReplaceRequest
from app.model.response.matting_resp import MattingResponse
import asyncio

human_matting = APIRouter()


@human_matting.post('/human-matting', response_model=MattingResponse, name="人像抠图")
async def human_matting(request: MattingRequest, service: MattingService = Depends(get_matting_service)):
    logger.info('开始人像抠图模型进行推理')
    loop = asyncio.get_event_loop()
    resp = await loop.run_in_executor(None,
                                      service.human_matting,
                                      request.img,
                                      request.max_width)
    return resp
