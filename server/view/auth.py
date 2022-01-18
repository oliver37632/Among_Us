from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from server.model.validator.auth import SendEmailCodeValidator, CheckEmailCodeValidator, SingupValidator, LoginValidator, CheckNickValidator
from server.view import validate_JSON
from server.controller.auht import singup, send_email, check_code, login, logout, token_refresh, check_nick


class Singup(Resource):
    @validate_JSON(SingupValidator)
    def post(self):
        email = request.json['email']
        nickname = request.json['nickname']
        password = request.json['password']

        return singup(
            email=email,
            nickname=nickname,
            password=password
        )


class Auth(Resource):
    @validate_JSON(LoginValidator)
    def post(self):
        nickname = request.json['nickname']
        password = request.json['password']

        return login(
            nickname=nickname,
            password=password
        )

    @jwt_required()
    def delete(self):
        nickname = get_jwt_identity()

        return logout(
            nickname=nickname
        )

    @jwt_required(refresh=True)
    def get(self):
        nickname = get_jwt_identity()
        return token_refresh(
            nickname=nickname
        )


class CheckNick(Resource):
    @validate_JSON(CheckNickValidator)
    def post(self):
        nickname = request.json['nickname']
        return check_nick(
            nickname=nickname
        )


class SendEmail(Resource):
    @validate_JSON(SendEmailCodeValidator)
    def post(self):
        email = request.json['email']
        return send_email(
            email=email
        )


class CheckCode(Resource):
    @validate_JSON(CheckEmailCodeValidator)
    def post(self):
        email = request.json['email']
        code = request.json['code']
        return check_code(
            email=email,
            code=code
        )