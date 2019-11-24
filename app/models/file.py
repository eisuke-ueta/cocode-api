from datetime import datetime

from app.database import db


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column('id', db.String(64), primary_key=True)
    user_id = db.Column('user_id', db.String(64), nullable=False)
    path = db.Column('path', db.String(255), unique=True, default='', nullable=False)
    name = db.Column('name', db.String(255), default='', nullable=False)
    media_type = db.Column('media_type', db.String(32), default='', nullable=False)
    size = db.Column('size', db.Integer, nullable=False)
    created_at = db.Column('created_at', db.DATETIME, default=datetime.now, nullable=False)
    updated_at = db.Column('updated_at', db.DATETIME, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return "<File '{}'>".format(self.id)
