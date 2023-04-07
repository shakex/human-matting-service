import os
import base64
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
from skimage import io
from io import BytesIO


def skew_correction(image, k_size=7):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    blur = cv2.GaussianBlur(gray, (k_size, k_size), 0)

    # setting all foreground pixels to 255 and all background pixels to 0
    ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    whereid = np.where(thresh > 0)
    # 交换横纵坐标的顺序，否则下面得到的每个像素点为(y,x)
    whereid = whereid[::-1]
    # 将像素点格式转换为(n_coords, 2)，每个点表示为(x,y)
    coords = np.column_stack(whereid)

    (x, y), (w, h), angle = cv2.minAreaRect(coords)
    if angle < -45:
        angle = 90 + angle

    vis = image.copy()
    box = cv2.boxPoints(((x, y), (w, h), angle))
    box = np.int0(box)
    # contours = cv2.drawContours(vis,[box],0,(0,0,255),2)

    # rotate the image to deskew it
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    # center = x, y  # 可以试试中心点设置为文本区域中心会是什么情况
    Mat = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, Mat, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    #     result = cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    return thresh, rotated, angle


def add_text(img, text, org, font_face, text_color=(0, 255, 0), text_size=15):
    if (isinstance(img, np.ndarray)):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_face, text_size, encoding="utf-8")
    draw.text(org, text, fill=text_color, font=font)

    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def imshow_ocr(img, words, bboxes, font, font_size=15, alpha=0.8, color=(0, 200, 255), fill=False):
    if not words or not bboxes:
        return img, img
    img_cp = img.copy()
    img_rec = np.zeros((img.shape[0], img.shape[1], 3), np.uint8) + 255
    for idx, item in enumerate(zip(words, bboxes)):
        lbl = str(idx + 1)
        word = item[0]
        bbox = item[1]
        offset = int((bbox[3] - bbox[1]) * 0.8)
        if fill:
            cv2.rectangle(img, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color, -1)
        else:
            cv2.rectangle(img, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color, 1)
            cv2.rectangle(img, (int(bbox[0] - offset - 10), int(bbox[1])), (int(bbox[0]), int(bbox[1] + offset)), color,
                          -1)
            cv2.putText(img, lbl, (int(bbox[0] - offset - 5), int(bbox[1] + 25)), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                        (0, 0, 0), 2)

        img_rec = add_text(img_rec, word, (bbox[0], bbox[1]), font_face=font, text_color=(0, 0, 0), text_size=font_size)
        cv2.rectangle(img_rec, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color, 1)
        cv2.rectangle(img_rec, (int(bbox[0] - offset - 10), int(bbox[1])), (int(bbox[0]), int(bbox[1] + offset)), color,
                      -1)
        cv2.putText(img_rec, lbl, (int(bbox[0] - offset - 5), int(bbox[1] + 25)), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                    (0, 0, 0), 2)

    if fill:
        img_det = cv2.addWeighted(img, 1 - alpha, img_cp, alpha, gamma=0)
    else:
        img_det = cv2.addWeighted(img, alpha, img_cp, 1 - alpha, gamma=0)

    img_det = img_det[:, :, ::-1]
    img_rec = img_rec[:, :, ::-1]

    return img_det, img_rec


def im_pair(img1, img2):
    img_pair = cv2.hconcat([img1, img2])
    return img_pair


def img_url_to_arr(url):
    image = io.imread(url)
    return image


def encode_b64(file):
    with open(file, 'rb') as f:
        img_data = f.read()
        base64_data = base64.b64encode(img_data)
        return base64_data.decode()


def decode_b64(base64_data, img_path='./im_b64.jpg'):
    with open(img_path, 'wb') as file:
        img = base64.b64decode(base64_data)
        file.write(img)
        return img


def decode_b64_to_arr(base64_data):
    img_data = base64.b64decode(base64_data)
    nparr = np.fromstring(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def encode_b64_from_file(file):
    """Convert filepath:`str` to base64 string."""
    with open(file, 'rb') as f:
        img_data = f.read()
        base64_data = base64.b64encode(img_data).decode("utf-8")
        return base64_data


def encode_b64_from_pil(image):
    """Convert PIL format(`PIL.Image.Image`) to base64 string."""
    img_buffer = BytesIO()
    image.save(img_buffer, format='JPEG')
    img_data = img_buffer.getvalue()
    base64_data = base64.b64encode(img_data).decode('utf-8')
    return base64_data


def encode_b64_from_cv2(image):
    """Convert cv2 image(`np.ndarry`) to base64 string."""
    img_data = cv2.imencode('.jpg', image)[1].tostring()
    base64_data = base64.b64encode(img_data).decode('utf-8')
    return base64_data


def encode_b64_from_bytes(image):
    """Convert `bytes` to base64 string."""
    base64_data = base64.b64encode(image).decode('utf-8')
    return base64_data


def encode_im_b64(image):
    """Convert image(`PIL.Image.Image` or `np.ndarry` or filepath:`str`) to base64 string."""
    if isinstance(image, str) and os.path.exists(image):
        img_b64 = encode_b64_from_file(image)
    elif isinstance(image, bytes):
        img_b64 = encode_b64_from_bytes(image)
    elif isinstance(image, Image.Image):
        img_b64 = encode_b64_from_pil(image)
    elif isinstance(image, np.ndarray):
        img_b64 = encode_b64_from_cv2(image)
    else:
        raise TypeError(f'Unsupported image format: {type(image)}')
    return img_b64
