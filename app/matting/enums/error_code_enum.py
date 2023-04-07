# reference: https://ai.baidu.com/ai-doc/OCR/dk3h7y5vr
import enum
from enum import unique


@unique
class ErrorCode(enum.Enum):
    # 未知错误，请再次请求，如果持续出现此类错误，请在控制台提交工单联系技术支持团队
    UNKNOWN_ERROR = 1

    # 服务暂不可用，请再次请求，如果持续出现此类错误，请在控制台提交工单联系技术支持团队
    SERVICE_TEMPORARILY_UNAVAILABLE = 2

    # 调用的API不存在，请检查请求URL后重新尝试，一般为URL中有非英文字符，如"-"，可手动输入重试
    UNSUPPORTED_OPENAPI_METHOD = 3

    # 集群超限额，请再次请求，如果持续出现此类错误，请在控制台提交工单联系技术支持团队
    OPEN_API_REQUEST_LIMIT_REACHED = 4

    # 无接口调用权限，创建应用时未勾选相关文字识别接口，请登录百度云控制台，找到对应的应用，编辑应用，勾选上相关接口后重新调用
    NO_PERMISSION_TO_ACCESS_DATA = 6

    # IAM鉴权失败，建议用户参照文档自查生成sign的方式是否正确，或换用控制台中ak sk的方式调用
    IAM_CERTIFICATION_FAILED = 14

    # 免费测试资源使用完毕，每天请求量超限额，已支持计费的接口，您可以在控制台文字识别服务选择购买相关接口的次数包或开通按量后付费；邀测和未支持计费的接口，您可以在控制台提交工单申请提升限额
    OPEN_API_DAILY_REQUEST_LIMIT_REACHED = 17

    # QPS超限额，免费额度并发限制为2QPS，开通按量后付费或购买次数包后并发限制为10QPS，如您需要更多的并发量，可以选择购买QPS叠加包；邀测和未支持计费的接口，您可以在控制台提交工单申请提升限额
    OPEN_API_QPS_REQUEST_LIMIT_REACHED = 18

    # 请求总量超限额，已支持计费的接口，您可以在控制台文字识别服务选择购买相关接口的次数包或开通按量后付费；邀测和未支持计费的接口，您可以在控制台提交工单申请提升限额
    OPEN_API_TOTAL_REQUEST_LIMIT_REACHED = 19

    # 无效的access_token参数，token拉取失败，您可以参考“Access Token获取”文档重新获取
    INVALID_PARAMETER = 100

    # access_token无效，token有效期为30天，请注意需要定期更换，也可以每次请求都拉取新token
    ACCESS_TOKEN_INVALID_OR_NO_LONGER_VALID = 110

    # access token过期，token有效期为30天，请注意需要定期更换，也可以每次请求都拉取新token
    ACCESS_TOKEN_EXPIRED = 111

    # 请求中包含非法参数，请检查后重新尝试
    INVALID_PARAM = 216100

    # 缺少必须的参数，请检查参数是否有遗漏
    NOT_ENOUGH_PARAM = 216101

    # 请求了不支持的服务，请检查调用的url
    SERVICE_NOT_SUPPORT = 216102

    # 请求中某些参数过长，请检查后重新尝试
    PARAM_TOO_LONG = 216103

    # appid不存在，请重新核对信息是否为后台应用列表中的appid
    APPID_NOT_EXIST = 216110

    # 图片为空，请检查后重新尝试
    EMPTY_IMAGE = 216200

    # 上传的图片格式错误，现阶段我们支持的图片格式为：PNG、JPG、JPEG、BMP，请进行转码或更换图片
    IMAGE_FORMAT_ERROR = 216201

    # 上传的图片大小错误，现阶段我们支持的图片大小为：base64编码后小于4M，分辨率不高于4096x4096，请重新上传图片
    IMAGE_SIZE_ERROR = 216202

    # 上传的包体积过大，现阶段不支持 10M 或以上的数据包
    INPUT_OVERSIZE = 216202

    # 识别错误，请再次请求，请确保图片中包含对应卡证票据
    RECOGNIZE_ERROR = 216230

    # 识别银行卡错误，出现此问题的原因一般为：您上传的图片非银行卡正面，上传了异形卡的图片、上传的银行卡正面图片不完整或模糊
    RECOGNIZE_BANK_CARD_ERROR = 216631

    # 识别身份证错误，出现此问题的原因一般为：您上传了非身份证图片、上传的身份证图片不完整或模糊
    RECOGNIZE_IDCARD_ERROR = 216633

    # 检测错误，请再次请求，如果持续出现此类错误，请在控制台提交工单联系技术支持团队
    DETECT_ERROR = 216634

    # 服务器内部错误，如果您使用的是高精度接口，报这个错误码的原因可能是您上传的图片中文字过多，识别超时导致的，建议您对图片进行切割后再识别，其他情况请再次请求， 如果持续出现此类错误，请在控制台提交工单联系技术支持团队
    INTERNAL_ERROR = 282000

    # 请求参数缺失
    MISSING_PARAMETERS = 282003

    # 处理批量任务时发生部分或全部错误，请根据具体错误码排查
    BATCH_PROCESSING_ERROR = 282005

    # 批量任务处理数量超出限制，请将任务数量减少到10或10以下
    BATCH_TASK_LIMIT_REACHED = 282006

    # 图片压缩转码错误
    IMAGE_TRANSCODE_ERROR = 282100

    # 未检测到图片中识别目标，请确保图片中包含对应卡证票据，出现此问题的原因一般为：您上传了非卡证图片、图片不完整或模糊
    TARGET_DETECT_ERROR = 282102

    # 图片目标识别错误，请确保图片中包含对应卡证票据，出现此问题的原因一般为：您上传了非卡证图片、图片不完整或模糊
    TARGET_RECOGNIZE_ERROR = 282103

    # URL参数不存在，请核对URL后再次提交
    URLS_NOT_EXIST = 282110

    # URL格式非法，请检查url格式是否符合相应接口的入参要求
    URL_FORMAT_ILLEGAL = 282111

    # url下载超时，请检查url对应的图床/图片无法下载或链路状况不好，或图片大小大于3M，或图片存在防盗链，您可以重新尝试以下，如果多次尝试后仍不行，建议更换图片地址
    URL_DOWNLOAD_TIMEOUT = 282112

    # URL返回无效参数
    URL_RESPONSE_INVALID = 282113

    # URL长度超过1024字节或为0
    URL_SIZE_ERROR = 282114

    # request id xxxxx 不存在
    REQUEST_ID_NOT_EXIST = 282808

    # 返回结果请求错误（不属于excel或json）
    RESULT_TYPE_ERROR = 282809

    # 图像识别错误，请再次请求，如果持续出现此类错误，请在控制台提交工单联系技术支持团队
    IMAGE_RECOGNIZE_ERROR = 282810
