from datetime import datetime

from app.database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column('id', db.String(64), primary_key=True)
    name = db.Column('name', db.String(100), nullable=False)
    email = db.Column('email', db.String(100), nullable=False, index=True, unique=True)
    alias = db.Column('alias', db.String(100), nullable=False, index=True, unique=True)
    avatar = db.Column('avatar', db.String(255))
    biography = db.Column('biography', db.String(255))
    password = db.Column('password', db.String(100), nullable=False)
    reset_password_token = db.Column('reset_password_token', db.String(100))
    reset_password_sent_at = db.Column('reset_password_sent_at', db.DATETIME)
    created_at = db.Column('created_at', db.DATETIME, default=datetime.now, nullable=False)
    updated_at = db.Column('updated_at', db.DATETIME, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return "<User '{}'>".format(self.id)
