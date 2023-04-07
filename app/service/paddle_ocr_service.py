from paddleocr import PaddleOCR


class PaddleOcrService:
    def __init__(self, **kwargs):
        self.ocr = PaddleOCR(**kwargs)

    def text_req(self, image, **kwargs):
        result = self.ocr.ocr(image, **kwargs)
        words = [item[1][0] for item in result]
        bboxes = [[item[0][0][0], item[0][0][1], item[0][2][0], item[0][2][1]] for item in result]
        confidence = [item[1][1] for item in result]
        return words, bboxes, confidence
