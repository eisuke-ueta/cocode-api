from typing import Dict, List, Optional

import shortuuid
from app.commons.logger import Logger
from app.models.user import User
from app.repositories.user_repository import UserRepository
from flask_bcrypt import Bcrypt


class UserService:

    UTF8 = "utf-8"

    def __init__(self, user_repository: UserRepository) -> None:
        self.logger = Logger(__name__)
        self.user_repository = user_repository
        self.bcrypt = Bcrypt()

    def get(self, offset: int, limit: int) -> List[User]:
        return self.user_repository.get(offset, limit, User.created_at.desc())

    def find(self, id: str) -> Optional[User]:
        return self.user_repository.find(id)

    def find_by_email(self, email: str) -> Optional[User]:
        return self.user_repository.find_by_email(email)

    def find_by_alias(self, alias: str) -> Optional[User]:
        return self.user_repository.find_by_alias(alias)

    def create(self, fields: Dict) -> Optional[User]:
        # Generate hash password
        hash_password = self.bcrypt.generate_password_hash(fields["password"]).decode(self.UTF8)
        fields["password"] = hash_password
        fields['alias'] = self._generate_alias()
        fields['avatar'] = "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"

        user = self.user_repository.create(fields)
        return user

    def _generate_alias(self) -> str:
        alias = str(shortuuid.uuid())
        while bool(self.user_repository.find_by_alias(alias)):
            alias = str(shortuuid.uuid())
        return alias

    def update(self, fields: Dict) -> Optional[User]:
        user = self.user_repository.find(fields["id"])
        new_user = self.user_repository.update(user, fields)
        return new_user

    def delete(self, id: str) -> Optional[User]:
        user = self.user_repository.find(id)
        if user:
            self.user_repository.delete(user)
        return user
