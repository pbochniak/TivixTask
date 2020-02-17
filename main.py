from hashlib import sha256

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.log import enable_pretty_logging


db = SQLAlchemy()
login_manager = LoginManager()


class Config:
    with open("/dev/urandom", "rb") as dev_random:
        SECRET_KEY = sha256(dev_random.read(100)).hexdigest()

    SQLALCHEMY_DATABASE_URI = "sqlite:///tmp/app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    with app.app_context():
        from task import routes

        db.create_all()
    return app


if __name__ == "__main__":
    enable_pretty_logging()
    server = HTTPServer(WSGIContainer(create_app()))
    server.listen(address="0.0.0.0", port=9999)
    IOLoop.instance().start()
