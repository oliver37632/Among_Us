from flask import Blueprint
from flask_restful import Api

bp = Blueprint("among", __name__, url_prefix="")
api_basic = Api(bp)

from server.view.auth import Singup
api_basic.add_resource(Singup, "/signup")

from server.view.auth import Auth
api_basic.add_resource(Auth, "/auth")

from server.view.auth import SendEmail
api_basic.add_resource(SendEmail, "/sendemail")

from server.view.auth import CheckCode
api_basic.add_resource(CheckCode, "/checkcode")

from server.view.auth import CheckNick
api_basic.add_resource(CheckNick, "/check")

from server.view.auth import FindId
api_basic.add_resource(FindId, "/findid")

