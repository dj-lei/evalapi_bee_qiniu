# coding:utf-8

from khas_core.rest import exceptions as khas_exc


class DealRecordErrorCode(khas_exc.ErrorCode):
    BAD_MODEL_DETAIL_SLUG = khas_exc.StatusCode(11000000001, '错误的款型')


class DealRecordException(khas_exc.GeneralException):
    pass
