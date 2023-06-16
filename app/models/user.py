from app import db
from flask_migrate import migrate
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    approved = db.Column(db.Boolean, default=False)

    def __init__(self, name, email, password,approved):
        self.name = name
        self.email = email
        self.password = password
        self.approved = approved


    def __repr__(self):
        return f"<User {self.email}>"