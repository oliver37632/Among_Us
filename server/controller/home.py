from flask import abort

from server.model import session_scope
from server.model.home import Home
from server.model.user import User
from server.model.s3 import s3_put_object, s3_connection
from server.config import AWS_S3_BUCKET_NAME

s3 = s3_connection()


def home(title, content, town, price, nickname):
    with session_scope() as session:
        new_home = Home(
            title=title,
            content=content,
            town=town,
            price=price,
            nickname=nickname
        )
        session.add(new_home)
        session.commit(new_home)

        name = new_home.idhoem
        s3_put_object(s3, AWS_S3_BUCKET_NAME, "./temp", name)
        location = s3.get_bucket_location(Bucket=AWS_S3_BUCKET_NAME)['LocationConstraint']
        image_url = f'https://{AWS_S3_BUCKET_NAME}.s3.{location}.amazonaws.com/{name}'

        new_home.image = image_url

        return {
                   "message": "success"
               }, 201


def pageGet(page_numbre):
    with session_scope() as session:
        limit = 10
        offset = limit * page_numbre

        home_list = session.query(Home, User) \
            .filter(Home.user_iduser == User.iduser) \
            .order_by(Home.created_at.desc()) \
            .limit(limit).offset(offset)

        next_home = session.query(Home).limit(1).offset(offset + limit)
        next_page = True if next_home else False

        return {
            "Homes": [{
                "nickname": User.nickname,
                "title": Home.title,
                "created_at": str(Home.created_at),
                "town": Home.town,
                "image": Home.image,
                "price": Home.price,
            } for User, home in home_list],
            "next_page": next_page
        }


def postGet(id):
    with session_scope() as session:
        homes = session.query(User.nickname,
                              Home.idhoem,
                              Home.title,
                              Home.content,
                              Home.created_at,
                              Home.town,
                              Home.category,
                              Home.image,
                              Home.price
                              ).join(User.iduser == Home.user_iduser).filter(Home.idhoem == id)
        if not home:
            abort(404, "Not Found")
        return {
            [{
                "nick": nick,
                "id": id,
                "title": title,
                "content": content,
                "created_at": str(created_at),
                "town": town,
                "category": category,
                "image": image,
                "price": price
            } for nick, id, title, content, created_at, town, category, image, price in homes]
        }


def homeDelete(id, nickname):
    with session_scope() as session:

        users = session.query(User).filter(User.nickname == nickname)
        if not users:
            abort(403, "You can't modify other users' posts.")

        homes = session.query(Home).filter(Home.idhoem == id)
        if not homes:
            abort(404, "Not Found")

        session.delete(homes)
        session.commit()

        s3.delete_object(Bucket=AWS_S3_BUCKET_NAME, Key=f'/temp.{id}')
        return {
                   "message": "success"
               }, 204


def homePatch(title, content, town, price, nickname, id):
    with session_scope() as session:

        homes = session.query(Home).filter(Home.idhoem == id)

        if not homes:
            abort(404, "Not Found")

        users = session.query(User).filter(User.nickname == nickname)

        if not users:
            abort(403, "You can't modify other users' posts")

        name = id
        s3_put_object(s3, AWS_S3_BUCKET_NAME, "./temp", name)
        location = s3.get_bucket_location(Bucket=AWS_S3_BUCKET_NAME)['LocationConstraint']
        image_url = f'https://{AWS_S3_BUCKET_NAME}.s3.{location}.amazonaws.com/{name}'

        homes.title = title,
        homes.content = content,
        homes.town = town,
        homes.price = price,
        homes.image = image_url

        return {
            "message": "success"
        }
