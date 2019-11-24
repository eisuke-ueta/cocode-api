from datetime import datetime

from app.database import db
from app.models.note_tag import NoteTag


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column('id', db.String(64), primary_key=True)
    name = db.Column('name', db.String(100), nullable=False, index=True)
    created_at = db.Column('created_at', db.DATETIME, default=datetime.now, nullable=False)
    updated_at = db.Column('updated_at', db.DATETIME, default=datetime.now, onupdate=datetime.now)

    notes = db.relationship(
        'Note', secondary=NoteTag.__tablename__, backref=db.backref('tag_notes', lazy=True), lazy='subquery')

    def __repr__(self):
        return "<Tag '{}'>".format(self.id)
