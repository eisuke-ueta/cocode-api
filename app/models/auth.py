from datetime import datetime

from app.database import db
from app.models.user import User


class Auth(db.Model):
    __tablename__ = 'auths'

    id = db.Column('id', db.String(64), primary_key=True)
    token = db.Column('token', db.String(255), index=True, unique=True)
    email = db.Column('email', db.ForeignKey(User.email), index=True, nullable=False)
    created_at = db.Column('created_at', db.DATETIME, default=datetime.now, nullable=False)

    user = db.relationship("User", backref=db.backref("auth_user", uselist=False), lazy='joined')

    def __repr__(self):
        return "<Auth '{}'>".format(self.id)
