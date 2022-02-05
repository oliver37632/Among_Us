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

from server.view.auth import Ping
api_basic.add_resource(Ping, "/")

from server.view.home import Home
api_basic.add_resource(Home, "/home")

from server.view.home import HomePostGet
api_basic.add_resource(HomePostGet, "/home/post/<int:id>")

from server.view.home import HomePageGet
api_basic.add_resource(HomePageGet, "/home/page/<int:page_numbre>")

from server.view.home import HomePost
api_basic.add_resource(HomePost, "/home/<int:id>")
