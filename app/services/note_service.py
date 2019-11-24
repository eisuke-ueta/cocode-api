from typing import Dict, List, Optional

from app.commons.logger import Logger
from app.models.note import Note
from app.models.tag import Tag
from app.repositories.note_repository import NoteRepository
from app.repositories.tag_repository import TagRepository


class NoteService:
    def __init__(self, note_repository: NoteRepository, tag_repository: TagRepository) -> None:
        self.logger = Logger(__name__)
        self.note_repository = note_repository
        self.tag_repository = tag_repository

    def get(self, offset: int, limit: int, user_id: str, status: str, keyword: str) -> List[Note]:
        status = status if status != 'all' else None
        return self.note_repository.get(
            offset=offset, limit=limit, order=Note.created_at.desc(), user_id=user_id, status=status, keyword=keyword)

    def count(self, user_id: str, status: str, keyword: str) -> int:
        status = status if status != 'all' else None
        notes = self.note_repository.count(
            order=Note.created_at.desc(), user_id=user_id, status=status, keyword=keyword)
        return len(notes)

    def find(self, id: str) -> Optional[Note]:
        return self.note_repository.find(id)

    def create(self, fields: Dict) -> Optional[Note]:
        fields["tags"] = self._create_tags(fields["tags"])
        note = self.note_repository.create(fields)

        return note

    def _create_tags(self, tag_names: List[str]) -> List[Tag]:
        tags = []
        for tag_name in tag_names:
            tag = self.tag_repository.find_by_name(tag_name)
            if not tag:
                tag = self.tag_repository.create({"name": tag_name})
            tags.append(tag)
        return tags

    def update(self, fields: Dict) -> Optional[Note]:
        fields["tags"] = self._create_tags(fields["tags"])
        note = self.note_repository.find(fields["id"])
        new_note = self.note_repository.update(note, fields)
        return new_note

    def delete(self, id: str) -> Optional[Note]:
        note = self.note_repository.find(id)
        if note:
            self.note_repository.delete(note)
        return note
