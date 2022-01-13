from flask import Blueprint
from flask_restful import Api

bp = Blueprint("among", __name__, url_prefix="")
api_basic = Api(bp)
