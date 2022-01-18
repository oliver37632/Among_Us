from flask import abort
from flask_jwt_extended import create_access_token, create_refresh_token

from werkzeug.security import generate_password_hash, check_password_hash

from server.model.user import User
from server.model import session_scope, Reids

import random


def singup(email, nicknaem, password):
    with session_scope() as session:
        origin = session.query.filter(User.email == email).scalar()
        if origin:
            return abort(409, "this email is use")

        new_user = User(
            email=email,
            nicknaem=nicknaem,
            password=generate_password_hash(password)
        )
        session.add(new_user)
        session.commit()

        return {
            "message": "success"
        }, 201


def login(nickname, password):
    with session_scope() as session:

        check_nick = session.query(User).filter(User.nickname == nickname)
        if not check_nick.scalar():
            abort(404, "email and password does not match")

        check_nick.first()
        check_password = check_password_hash(User.password, password)
        if not check_password:
            abort(404, "password and emaill does not match")

        access_token = create_access_token(identity=nickname)
        refresh_token = create_refresh_token(identity=nickname)

        Reids.setex(name=nickname,
                    value=refresh_token,
                    time=604800)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
                },200


def logout(nickname):
    token = Reids.get(nickname)
    if not token:
        return abort(401, "cloud not find token user")
    Reids.delete(token)

    return {
        "message":"success"
    }, 204

def send_email(email):
    with session_scope() as session:
        user = session.query(User).filter(User.email == email).scalar()

        if not user:
            abort(409, "this email is already in use")

        code = f"{random.randint(1111, 9999):04d}"
        title = "AOMGAS_US 이메일 인증 메일"
        content = f"이메일 인증 코드는 {code}입니다."

        send_email(code=code,
                   title=title,
                   content=content
                   )
        Reids.setx(name=email,
                   value=code,
                   time=180)

        return {
            "message":"success"
        }, 200


def check_code(email, code):
    get_code = Reids.get(email)
    if not get_code:
        abort(404, 'this email does not exist')
    if int(get_code) != int(code):
        abort(409, 'email and code does not match')

        return {
            "message": "success"
        }, 200


def check_nick(nickname):
    with session_scope() as session:
        user = session.query(User).filter(User.nickname == nickname).scalar()

        if user:
            abort(409, "this nockname is use")

        return {
            "message": "can use this nickname"
        }, 200


def token_refresh(nickname):
    access_token = create_access_token(identity=nickname)

    return {
        "access_token": access_token
    }, 201