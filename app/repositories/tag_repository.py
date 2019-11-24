from app.models.tag import Tag
from app.repositories.base_repository import BaseRepository


class TagRepository(BaseRepository):
    model_class = Tag

    def find_by_name(self, name: str) -> Tag:
        return self.model_class.query.filter_by(name=name).first()
