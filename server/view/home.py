from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from server.model.validator.home import PostValidator
from server.view import validate_JSON
from server.controller.home import home, pageGet, postGet, homeDelete, homePatch


class Home(Resource):
    @jwt_required()
    @validate_JSON(PostValidator)
    def post(self):
        title = request.form['title']
        content = request.form['content']
        town = request.form['town']
        price = request.form['price']
        image = request.files['image']
        image.save("./temp")
        nickname = get_jwt_identity()

        return home(
            title=title,
            content=content,
            town=town,
            price=price,
            nickname=nickname
        )


class PageGet(Resource):
    def get(self, page_numbre):
        return pageGet(
            page_numbre=page_numbre
        )


class PostGet(Resource):
    @jwt_required()
    def get(self, id):
        return postGet(
            id=id,
            nickname=get_jwt_identity()
        )


class HomePost(Resource):
    @jwt_required()
    def delete(self, id):
        nickname = get_jwt_identity()
        return homeDelete(
            id=id,
            nickname=nickname
        )

    @jwt_required()
    def patch(self, id):
        title = request.form['title']
        content = request.form['content']
        town = request.form['town']
        price = request.form['price']
        image = request.files['image']
        image.save("./temp")
        nickname = get_jwt_identity()
        return homePatch(
            title=title,
            content=content,
            town=town,
            price=price,
            nickname=nickname,
            id=id
        )
