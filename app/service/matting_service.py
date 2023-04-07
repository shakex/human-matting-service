import os
import json
import time
import sys
from loguru import logger
from fastapi import HTTPException
from app.utils.utils import *
import paddle
from app.model.response.matting_resp import MattingResponse
from paddleseg.utils import get_sys_env
from paddleseg.cvlibs import manager, Config
from paddleseg import utils
from app.service.Matting import predict, Compose

manager.BACKBONES._components_dict.clear()
manager.TRANSFORMS._components_dict.clear()


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


class MattingService:
    def __init__(self, config='../../config.json'):
        with open(config) as json_file:
            self.config = json.load(json_file)
        self.config_file = self.config['model_config']
        self.model_path = self.config["model_path"]
        self.trimap = self.config["trimap_path"]
        self.fg_estimate = self.config["fg_estimate"]
        self.log_path = os.path.join(self.config['log_dir'], '{time:YYYY-MM-DD}.log')
        logger.add(self.log_path, rotation=should_rotate_by_day, enqueue=True)

        cfg = Config(self.config_file)

        msg = '\n---------------Config Information---------------\n'
        msg += str(cfg)
        msg += '------------------------------------------------'
        logger.info(msg)

        print(os.path.abspath(self.config_file))
        self.transforms = Compose(cfg.val_transforms)
        self.model = cfg.model
        utils.utils.load_entire_model(self.model, self.model_path)
        self.model.eval()

    @staticmethod
    def get_response(rgba: str = ""):
        matting_response = MattingResponse(rgba=rgba)
        return matting_response

    def human_matting(self, url: str = None, max_width: int = None):
        if not url:
            logger.error(f'error')

        env_info = get_sys_env()
        place = 'gpu' if env_info['Paddle compiled with cuda'] and env_info[
            'GPUs used'] else 'cpu'

        paddle.set_device(place)
        if not self.config_file:
            raise RuntimeError('No configuration file specified.')

        if not self.trimap:
            trimap_list = None
        else:
            trimap_list = [self.trimap]

        try:
            alpha_pred, fg = predict(self.model,
                                     model_path=self.model,
                                     transforms=self.transforms,
                                     image_list=[url],
                                     trimap_list=trimap_list,
                                     fg_estimate=self.fg_estimate)
        except Exception as e:
            logger.error(f'exe prediction error: {e}')
            raise Exception(e)

        result_b64 = encode_b64_from_cv2(alpha_pred)

        resp = self.get_response(result_b64)
        return resp


def get_matting_service():
    return MattingService()


if __name__ == '__main__':
    service = MattingService()
    url = '/home/pudding/data/project/pp-matting-service/imgs/test1.png'
    resp = service.human_matting(url)
