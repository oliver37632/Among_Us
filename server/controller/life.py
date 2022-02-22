import random

from flask import abort, request

from uuid import uuid4

from server.model import session_scope
from server.model.life import Life
from server.model.user import User
from server.model.s3 import s3_put_object, s3, get_url
from server.config import AWS_S3_BUCKET_NAME


def life(content, town, nickname, category):
    with session_scope() as session:
        new_Life = Life(
            content=content,
            town=town,
            nickname=nickname,
            category=category
        )
        session.add(new_Life)
        session.commit()

        return {
                   "message": "success"
               }, 201


def image(image):

    name = str(uuid4())
    s3_put_object(image, name)

    image_url = get_url(name)

    return {
        "url": image_url
    }, 201


def pageGet(page_numbre):
    with session_scope() as session:
        limit = 10
        offset = limit * page_numbre

        Life_list = session.query(Life, User) \
            .filter(Life.nickname == User.nickname) \
            .order_by(Life.created_at.desc()) \
            .limit(limit).offset(offset)

        next_Life = session.query(Life).limit(1).offset(offset + limit).scalar()
        next_page = True if next_Life else False

        return {
            "Lifes": [{
                "created_at": str(Life.created_at),
                "town": Life.town,
                "image": Life.image,
                "nickname": user.nickname,
            } for Life, user in Life_list],
            "next_page": next_page
        }


def postGet(id):
    with session_scope() as session:
        Lifes = session.query(User.nickname,
                              Life.Id_Life,
                              Life.content,
                              Life.created_at,
                              Life.town,
                              Life.category,
                              Life.image,
                              ).join(User, User.nickname == Life.nickname).filter(Life.Id_Life == id)
        if not Life:
            abort(404, "Not Found")
        return {
            "Life": [{
                "nick": nick,
                "id": id,
                "content": content,
                "created_at": str(created_at),
                "town": town,
                "category": category,
                "image": image,
            } for nick, id, content, created_at, town, category, image in Lifes]
        }, 200


def lifeDelete(id, nickname):
    with session_scope() as session:

        del_Lifes = session.query(Life).filter(Life.Id_Life == id, Life.nickname == nickname)

        if not del_Lifes.scalar():
            abort(404, 'could not find post matching this id or nickname')

        del_Lifes = del_Lifes.first()

        # s3.delete_object(Bucket=AWS_S3_BUCKET_NAME, Key=str(id))

        session.delete(del_Lifes)
        session.commit()

        return {
                   "message": "success"
               }, 204


def lifePatch(content, town, nickname, id, image):
    with session_scope() as session:

        Lifes = session.query(Life).filter(Life.Id_Life == id)

        if not Lifes:
            abort(404, "Not Found")

        users = session.query(User).filter(User.nickname == nickname)

        if not users:
            abort(403, "You can't modify other users' posts")

        name = str(uuid4())
        s3_put_object(image, name)

        image_url = get_url(name)

        Lifes.content = content,
        Lifes.town = town,
        Lifes.image = image_url

        return {
            "message": "success"
        }


def follow(id, nickname):
