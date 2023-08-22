# -*- coding: utf8 -*-

from werkzeug.exceptions import HTTPException


class AppError(HTTPException):
    # http status code
    status_code = 200
    # app custom code
    code: str

    def __init__(self, msg, data=None):
        super().__init__()
        self.msg = msg
        self.data = data

    def to_json(self):
        return self._render_json(self.data, self.code, self.msg)

    @classmethod
    def internal_error_json(cls, e):
        return cls._render_json(None, '500', 'Internal Server Error')

    @staticmethod
    def _render_json(data, code='0', msg='ok'):
        return {'code': code, 'msg': msg, 'data': data}


class ArgumentMissing(AppError):
    code = '10010001'


class InvalidArgument(AppError):
    code = '10010002'


class UnrecognizedHost(AppError):
    code = '10020001'


class UnrecognizedRepo(AppError):
    code = '10020002'
