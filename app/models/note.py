from datetime import datetime

from app.database import db
from app.models.note_tag import NoteTag


class Note(db.Model):
    __tablename__ = 'notes'

    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'
    SALE_TYPE_FREE = "free"
    SALE_TYPE_PAY_AS_USE = "pay_as_use"

    id = db.Column('id', db.String(64), primary_key=True)
    user_id = db.Column('user_id', db.ForeignKey("users.id"), nullable=False)
    title = db.Column('title', db.String(255))
    description = db.Column('description', db.TEXT)
    status = db.Column('status', db.String(32), nullable=False)
    created_at = db.Column('created_at', db.DATETIME, default=datetime.now, nullable=False)
    updated_at = db.Column('updated_at', db.DATETIME, default=datetime.now, onupdate=datetime.now)

    user = db.relationship("User", backref=db.backref("note_user", uselist=False), lazy='joined')
    tags = db.relationship(
        'Tag', secondary=NoteTag.__tablename__, backref=db.backref('note_tags', lazy=True), lazy='subquery')

    def __repr__(self):
        return "<Note '{}'>".format(self.id)
