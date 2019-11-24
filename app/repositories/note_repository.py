from typing import Any, List

import shortuuid
from app.models.note import Note
from app.repositories.base_repository import BaseRepository


class NoteRepository(BaseRepository):
    model_class = Note

    def get(self,
            offset: int,
            limit: int,
            order: Any = None,
            user_id: str = None,
            status: str = None,
            keyword: str = None) -> List[Note]:
        query = self.model_class.query
        if order is not None:
            query = query.order_by(order)
        if status is not None:
            query = query.filter_by(status=status)
        if user_id is not None:
            query = query.filter_by(user_id=user_id)
        if keyword is not None:
            query = query.filter(Note.title.contains(keyword) | Note.description.contains(keyword))

        return query.offset(offset).limit(limit).all()

    def count(self, order: Any = None, user_id: str = None, status: str = None, keyword: str = None) -> List[Note]:
        query = self.model_class.query
        if order is not None:
            query = query.order_by(order)
        if status is not None:
            query = query.filter_by(status=status)
        if user_id is not None:
            query = query.filter_by(user_id=user_id)
        if keyword is not None:
            query = query.filter(Note.title.contains(keyword) | Note.description.contains(keyword))

        return query.all()

    # def create(self, fields: Dict) -> Note:
    #     fields['id'] = self._generate_id()

    #     model = self.model_class(**fields)
    #     self.session.add(model)
    #     self.session.commit()
    #     return model

    # def _generate_id(self) -> str:
    #     id_ = str(shortuuid.uuid())
    #     while self.exist(id_):
    #         id_ = str(shortuuid.uuid())
    #     return id_
