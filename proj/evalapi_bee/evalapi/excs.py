from rest_framework import exceptions
from rest_framework import status
from kkconst import BaseConst, ConstIntField


class ErrorCodeException(Exception):
    pass


class ErrorCodeNotProvided(ErrorCodeException):
    pass


class ErrorCode(BaseConst):
    class Meta:
        allow_duplicated_value = False
        strict_capital = True


StatusCode = ConstIntField

# 错误码分配原则：
# 系统基本错误码: 4位数，如果是HTTP标准状态码就在状态码中间加一个0
# 应用错误码: 100016001, 100 - 应用码区分项目， 01 - 区分模块，6001 - 具体错误码
# 见https://trello.com/c/qv05rVJ0


class BasicErrorCodes(ErrorCode):
    VALIDATION_ERROR = StatusCode(1001)
    MIN_LENGTH_ERROR = StatusCode(1002)
    MAX_LENGTH_ERROR = StatusCode(1003)
    FIELD_REQUIRED = StatusCode(1004)
    NULL_FIELD = StatusCode(1005)
    BLANK_FIELD = StatusCode(1006)
    EMPTY_FIELD = StatusCode(1007)
    NO_NAME = StatusCode(1008)
    INVALID_IMAGE = StatusCode(1009)
    DOES_NOT_EXIST = StatusCode(1010)
    INCORRECT_TYPE = StatusCode(1011)
    INCORRECT_MATCH = StatusCode(1012)
    NO_MATCH = StatusCode(1013)
    INVALID_CHOICE = StatusCode(1014)
    NOT_A_LIST = StatusCode(1015)
    DATE_ERROR = StatusCode(1016)
    DATETIME_ERROR = StatusCode(1017)

    PARSE_ERROR = StatusCode(400)
    UNAUTHENTICIZED = StatusCode(401)
    PERMISSION_DENIED = StatusCode(403)
    NOT_FOUND = StatusCode(404)
    METHOD_NOT_ALLOWED = StatusCode(405)
    NOT_ACCEPTABLE = StatusCode(406)
    UNSUPPORTED_MEDIA_TYPE = StatusCode(415)
    THROTTLED = StatusCode(429)


BASE_EXCEPTION_CODE_MAP = {
    'invalid': BasicErrorCodes.VALIDATION_ERROR,
    'min_length': BasicErrorCodes.MIN_LENGTH_ERROR,
    'max_length': BasicErrorCodes.MAX_LENGTH_ERROR,
    'required': BasicErrorCodes.FIELD_REQUIRED,
    'null': BasicErrorCodes.NULL_FIELD,
    'blank': BasicErrorCodes.BLANK_FIELD,
    'empty': BasicErrorCodes.EMPTY_FIELD,
    'no_name': BasicErrorCodes.NO_NAME,
    'invalid_image': BasicErrorCodes.INVALID_IMAGE,
    'does_not_exist': BasicErrorCodes.DOES_NOT_EXIST,
    'incorrect_type': BasicErrorCodes.INCORRECT_TYPE,
    'incorrect_match': BasicErrorCodes.INCORRECT_MATCH,
    'no_match': BasicErrorCodes.NO_MATCH,
    'invalid_choice': BasicErrorCodes.INVALID_CHOICE,
    'not_a_list': BasicErrorCodes.NOT_A_LIST,
    'date': BasicErrorCodes.DATE_ERROR,
    'datetime': BasicErrorCodes.DATETIME_ERROR,

    'parse_error': BasicErrorCodes.PARSE_ERROR,
    'authentication_failed': BasicErrorCodes.UNAUTHENTICIZED,
    'not_authenticated': BasicErrorCodes.UNAUTHENTICIZED,
    'permission_denied': BasicErrorCodes.PERMISSION_DENIED,
    'not_found': BasicErrorCodes.NOT_FOUND,
    'method_not_allowed': BasicErrorCodes.METHOD_NOT_ALLOWED,
    'not_acceptable': BasicErrorCodes.NOT_ACCEPTABLE,
    'unsupported_media_type': BasicErrorCodes.UNSUPPORTED_MEDIA_TYPE,
    'throttled': BasicErrorCodes.THROTTLED
}


class GeneralException(exceptions.APIException):
    """
    通用exception类，支持code体系
    """
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, code, status_code=None, **kwargs):
        detail = code.verbose_name.format(**kwargs)
        super(GeneralException, self).__init__(code=code, detail=detail)

        self.status_code = status_code if status_code else self.status_code

