from flask_login import UserMixin

from main import db
from task.misc import getRandomHash, saltWord


class User(UserMixin, db.Model):
    __tablename__ = "users"
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    saltedPassword = db.Column(db.String, nullable=False)
    salt = db.Column(db.String, nullable=False)

    def __init__(self, name, password):
        self.name = name
        self.setPassword(password)

    def setPassword(self, password):
        self.salt = getRandomHash()
        self.saltedPassword = saltWord(password, self.salt)

    def checkPassword(self, password):
        return self.saltedPassword == saltWord(password, self.salt)

    @staticmethod
    def validate(body):
        return "username" in body and "password" in body and len(body) == 2
