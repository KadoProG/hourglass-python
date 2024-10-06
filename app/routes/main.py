from flask import Blueprint
from app.controllers.main import index, start, angle

main_bp = Blueprint("main", __name__)

main_bp.route("/", methods=["GET"])(index)
main_bp.route("/start", methods=["GET"])(start)
main_bp.route("/angle", methods=["GET"])(angle)
