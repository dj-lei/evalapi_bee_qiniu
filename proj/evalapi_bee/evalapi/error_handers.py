# -*- encoding: utf-8 -*-
# 用于函数计算独立的错误处理
import six
from rest_framework import exceptions
from rest_framework.compat import set_rollback


def exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait
        errors = exc.detail
        if isinstance(exc.detail, list):
            error_detail = exc.detail[0]
        elif isinstance(exc.detail, dict):
            # TODO 处理嵌套字典的错误,嵌套serializer中会出现此种情况，对于嵌套的报错，使用最里层的那个报错字符串
            error_detail = exc.detail.copy().popitem()[1][0]
            set_rollback()
        else:
            error_detail = exc.detail
            errors = None

        error_code = getattr(error_detail, 'code', 'invalid')

        if isinstance(error_code, six.text_type):
            error_code = 1001

        set_rollback()
        if error_code < 1000:
            # drf内部错误有时通过error_detail中获取的code和实际http应该返回的code不一致，所以如果不是验证错误
            # 使用exc的status_code作为返回码
            error_code = exc.status_code
        return {'code': error_code, 'detail': error_detail, 'errors': errors}

    return {'code': -1, 'detail': 'unknown'}
