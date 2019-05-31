# coding:utf-8
try:
    from evalapi import excs as exc
except ImportError:
    from khas_core.rest import exceptions as exc

# provide exception processing with error code system


class EvalApiException(exc.GeneralException):
    pass


class EvalApiErrorCode(exc.ErrorCode):
    BAD_CITY = exc.StatusCode(101000001, '不支持的城市')
    BAD_REG_DATE = exc.StatusCode(101000002, '上牌时间应该在过去的20年内')
    BAD_MODEL_DETAIL_SLUG = exc.StatusCode(101000003, '款型不合法')


VALUATION_ERROR_MAP = {
    'model_detail_slug': EvalApiErrorCode.BAD_MODEL_DETAIL_SLUG,
    'use_time': EvalApiErrorCode.BAD_REG_DATE,
    'city': EvalApiErrorCode.BAD_CITY,
    'model_detail_slug or city': EvalApiErrorCode.BAD_MODEL_DETAIL_SLUG
}




