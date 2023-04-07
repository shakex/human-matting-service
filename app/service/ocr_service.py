import os
import json
import time
import sys
from loguru import logger
from fastapi import HTTPException
from .paddle_ocr_service import PaddleOcrService
from app.utils.utils import *
from app.model.response.general_text_resp import GeneralTextResponse, WordResult


def should_rotate_by_hour(message, file):
    filepath = os.path.abspath(file.name)
    creation = os.path.getctime(filepath)
    now = message.record["time"].timestamp()
    maxtime = 60 * 60  # 1 hour in seconds
    return now - creation > maxtime


# 每天生成一个
def should_rotate_by_day(message, file):
    filepath = os.path.abspath(file.name)
    creation_timestamp = os.path.getctime(filepath)
    now_timestamp = message.record["time"].timestamp()
    # 当前日志创建时间和当前时间不是同一天，则新创建
    create = time.strftime("%Y-%m-%d", time.localtime(creation_timestamp))
    now = time.strftime("%Y-%m-%d", time.localtime(now_timestamp))
    if now == create:
        return False
    else:
        return True


class OCRService:
    def __init__(self, config='../config.json'):
        with open(config) as json_file:
            self.config = json.load(json_file)
        self.service_name = self.config['service']
        self.log_path = os.path.join(self.config['log_dir'], '{time:YYYY-MM-DD}.log')
        logger.add(self.log_path, rotation=should_rotate_by_day, enqueue=True)

        if self.service_name == 'paddle':
            self.service = PaddleOcrService(**self.config['paddle']['service'])
            logger.info('init paddleocr service success.')
        else:
            raise NotImplementedError(f'Service {self.service_name} not supported yet.')

    @staticmethod
    def get_response(image_width, image_height, words, bboxes, confidence, direction: float = 0.0, result_b64: str = ""):
        result = []
        word_count = len(words)
        for i in range(word_count):
            word_result = WordResult(text=words[i],
                                     location=[int(bboxes[i][0]),
                                               int(bboxes[i][1]),
                                               int(bboxes[i][2]),
                                               int(bboxes[i][3])],
                                     confidence=confidence[i])
            result.append(word_result)

        general_text_response = GeneralTextResponse(width=image_width,
                                                    height=image_height,
                                                    draw_result=result_b64,
                                                    word_count=word_count,
                                                    direction=direction,
                                                    result=result)

        return general_text_response

    def recognize_general_text(self, image: str = None, url: str = None, max_width: int = None, draw_result: bool = False, detect_direction: bool = False):
        if not image and not url:
            logger.error(f'error')

        if image:
            if os.path.isfile(image):
                image_arr = cv2.imread(image)[:, :, ::-1]
            else:
                image_arr = decode_b64_to_arr(image)
        elif url:
            try:
                image_arr = img_url_to_arr(url)
            except Exception as e:
                logger.error(f'fetch image from url error: {e}')
                # raise HTTPException(status_code=, detail='', headers={"X-Error"})


        image_width = image_arr.shape[1]
        image_height = image_arr.shape[0]
        if max_width and image_width > max_width:
            image_ocr = cv2.resize(image_arr, dsize=(max_width, int(image_height*max_width/image_width)), interpolation=cv2.INTER_LINEAR)
        else:
            image_ocr = image_arr

        try:
            words, bboxes, confidence = self.service.text_req(image_ocr, **self.config[self.service_name]['method'])
        except Exception as e:
            logger.error(f'recognize general text error: {e}')
            raise Exception(e)


        result_b64 = ""
        cv2_image = image_arr[:, :, ::-1]
        if draw_result:
            draw_font = self.config['draw_font']
            image_det, image_rec = imshow_ocr(cv2_image, words, bboxes, draw_font)
            img_pair = im_pair(image_det, image_rec)
            result_b64 = encode_b64_from_cv2(img_pair[:, :, ::-1])

        direction = 0.0
        # if detect_direction:
        #     # todo: direction
        #     pass

        resp = self.get_response(image_width, image_height, words, bboxes, confidence, direction=direction, result_b64=result_b64)
        return resp


def get_ocr_service():
    return OCRService()
