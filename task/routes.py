from flask import Blueprint, request, abort

# redirect, flash, Blueprint, request, session, url_for, abort
from flask_login import login_required, logout_user, current_user, login_user

from main import db
from task.models import User

usersBP = Blueprint("usersBP", __name__)
moviesBP = Blueprint("moviesBP", __name__)


@login_required
@usersBP.route("/whoami", methods=["POST"])
def getCurrentUser():
    pass


@usersBP.route("/login", methods=["POST"])
def logIn():
    if current_user.is_authenticated:
        abort(400, "Already logged in")
    body = request.json
    if not body:
        abort(400, "Missing request body")
    if not User.validate(body):
        abort(400, "Missing one of key [name, password] in request body")
    user = User.query.filter_by(name=body["username"]).first()
    if not user:
        abort(400, "Unknown user's name")
    if not user.checkPassword(body["password"]):
        abort(400, "Bad password")
    login_user(user)
    return f"Logged in as {user.name}"


@login_required
@usersBP.route("/logout", methods=["POST"])
def logOut():
    logout_user()
    return "Logged out"


@usersBP.route("/signup", methods=["POST"])
def signUp():
    if current_user.is_authenticated:
        abort(400, "Already logged in")
    body = request.json
    if not body:
        abort(400, "Missing request body")
    body = request.json
    if not User.validate(body):
        abort(400, "Missing one of key [name, password] in request body")
    user = User.query.filter_by(name=body["username"]).first()
    if user:
        abort(400, "User '{}' already exists")
    user = User(body["username"], body["password"])
    db.session.add(user)
    db.session.commit()
    return f"Account '{user.name}' created"


@login_required
@moviesBP.route("/search", methods=["GET"])
def search():
    return "TODO"


@login_required
@moviesBP.route("/movie", methods=["GET"])
def getMovie():
    return "TODO"


@login_required
@moviesBP.route("/favorites", methods=["GET"])
def getFavorites():
    return "TODO"


@login_required
@moviesBP.route("/favorites", methods=["PUT"])
def putFavorite():
    return "TODO"


@login_required
@moviesBP.route("/favorites", methods=["DELETE"])
def removeFavorite():
    return "TODO"
