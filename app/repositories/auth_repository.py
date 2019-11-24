from app.models.auth import Auth
from app.repositories.base_repository import BaseRepository


class AuthRepository(BaseRepository):
    model_class = Auth

    def find_by_token(self, token: str) -> Auth:
        return self.model_class.query.filter_by(token=token).first()

    def find_by_email(self, email: str) -> Auth:
        return self.model_class.query.filter_by(email=email).first()
