from typing import Dict

from app.models.note import Note
from app.vos.tag_vo import TagVo
from app.vos.user_vo import UserVo


class NoteVo:
    def __init__(self, note: Note) -> None:
        self.note = note

    def to_dict(self) -> Dict:
        return {
            "id": self.note.id,
            "user": UserVo(self.note.user).to_dict(),
            "title": self.note.title,
            "tags": [TagVo(tag).to_dict() for tag in self.note.tags],
            "description": self.note.description,
            "status": self.note.status,
            "createdAt": self.note.created_at,
            "updatedAt": self.note.updated_at
        }
