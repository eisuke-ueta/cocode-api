from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    model_class = User

    def find_by_email(self, email: str) -> User:
        return self.model_class.query.filter_by(email=email).first()

    def find_by_alias(self, alias: str) -> User:
        return self.model_class.query.filter_by(alias=alias).first()
