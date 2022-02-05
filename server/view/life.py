from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from server.controller.life import life, pageGet, postGet, lifeDelete, lifePatch


class Life(Resource):
    @jwt_required()
    def post(self):
        content = request.form['content']
        town = request.form['town']
        category = request.form['category']
        image = request.files['image']
        image.save("./temp")
        nickname = get_jwt_identity()

        return life(
            content=content,
            town=town,
            nickname=nickname,
            category=category
        )


class LifePageGet(Resource):
    def get(self, page_numbre):
        return pageGet(
            page_numbre=page_numbre
        )


class LifePostGet(Resource):
    @jwt_required()
    def get(self, id):
        return postGet(
            id=id,
        )


class LifePost(Resource):
    @jwt_required()
    def delete(self, id):
        nickname = get_jwt_identity()
        return lifeDelete(
            id=id,
            nickname=nickname
        )

    @jwt_required()
    def patch(self, id):
        content = request.form['content']
        town = request.form['town']
        image = request.files['image']
        image.save("./temp")
        nickname = get_jwt_identity()
        return lifePatch(
            content=content,
            town=town,
            nickname=nickname,
            id=id
        )
