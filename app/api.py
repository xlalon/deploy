# -*- coding: utf8 -*-

from flask import request
from flask_restful import Resource, Api

from .exception import AppError, ArgumentMissing

NullObject = object()


class AppResource(Resource):

    # noinspection PyMethodMayBeStatic
    def get_argument(self, arg: str, strict=True, type_=None, default=None):
        result = request.args.get(arg, NullObject)
        if result is NullObject and request.content_type == 'application/json':
            result = request.json.get(arg, NullObject)
        if result is NullObject:
            result = request.form.get(arg, NullObject)
        if result is NullObject:
            if strict:
                raise ArgumentMissing(f'arg `{arg}` missing')
            result = default
        if type_ is not None:
            try:
                result = type_(result)
            except ValueError:
                result = default

        return result

    # noinspection PyMethodMayBeStatic
    def render_json(self, data, code='0', msg='ok'):
        return {'code': code, 'msg': msg, 'data': data}


class AppApi(Api):
    def handle_error(self, e):
        if isinstance(e, AppError):
            return e.to_json()
        return AppError.internal_error_json(e)
