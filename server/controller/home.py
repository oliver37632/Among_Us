from flask import abort

from server.model import session_scope
from server.model.home import Home
from server.model.user import User
from server.model.s3 import s3_put_object, s3_connection
from server.config import AWS_S3_BUCKET_NAME

s3 = s3_connection()


def home(title, content, town, price, nickname, category):
    with session_scope() as session:
        new_home = Home(
            title=title,
            content=content,
            town=town,
            price=price,
            nickname=nickname,
            category=category
        )
        session.add(new_home)
        session.commit()

        name = str(new_home.Id_home)
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
            .filter(Home.nickname == User.nickname) \
            .order_by(Home.created_at.desc()) \
            .limit(limit).offset(offset)

        next_home = session.query(Home).limit(1).offset(offset + limit).scalar()
        next_page = True if next_home else False

        return {
            "Homes": [{
                "title": home.title,
                "created_at": str(home.created_at),
                "town": home.town,
                "image": home.image,
                "price": home.price,
                "nickname": user.nickname,
            } for home, user in home_list],
            "next_page": next_page
        }


def postGet(id):
    with session_scope() as session:
        homes = session.query(User.nickname,
                              Home.Id_home,
                              Home.title,
                              Home.content,
                              Home.created_at,
                              Home.town,
                              Home.category,
                              Home.image,
                              Home.price
                              ).join(User, User.nickname == Home.nickname).filter(Home.Id_home == id)
        if not home:
            abort(404, "Not Found")
        return {
            "Home": [{
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
        }, 200


def homeDelete(id, nickname):
    with session_scope() as session:

        del_homes = session.query(Home).filter(Home.Id_home == id, Home.nickname == nickname)

        if not del_homes.scalar():
            abort(404, 'could not find post matching this id or nickname')

        del_homes = del_homes.first()

        s3.delete_object(Bucket=AWS_S3_BUCKET_NAME, Key=str(id))

        session.delete(del_homes)
        session.commit()

        return {
                   "message": "success"
               }, 204


def homePatch(title, content, town, price, nickname, id):
    with session_scope() as session:

        homes = session.query(Home).filter(Home.Id_home == id)

        if not homes:
            abort(404, "Not Found")

        users = session.query(User).filter(User.nickname == nickname)

        if not users:
            abort(403, "You can't modify other users' posts")

        name = str(id)
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
