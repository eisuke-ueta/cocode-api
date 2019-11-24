from app.database import db


class NoteTag(db.Model):
    __tablename__ = 'note_tag'

    note_id = db.Column('note_id', db.ForeignKey("notes.id"), primary_key=True)
    tag_id = db.Column('tag_id', db.ForeignKey("tags.id"), primary_key=True)

    def __repr__(self):
        return "<NoteTag '{}'>".format(self.id)
