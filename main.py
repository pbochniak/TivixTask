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
        from task.routes import usersBP, moviesBP

        app.register_blueprint(usersBP, url_prefix="/api")
        app.register_blueprint(moviesBP, url_prefix="/api")
        from task.models import User

        @login_manager.user_loader
        def load_user(userID):
            if userID is not None:
                return User.query.get(uid=userID)
            return None

        print("A")
        db.create_all()
        db.session.commit()
        print("B")
    return app


if __name__ == "__main__":
    enable_pretty_logging()
    server = HTTPServer(WSGIContainer(create_app()))
    server.listen(address="0.0.0.0", port=9999)
    IOLoop.instance().start()
