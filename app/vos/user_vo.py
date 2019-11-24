from typing import Dict

from app.commons.config import Config
from app.models.user import User


class UserVo:
    def __init__(self, user: User) -> None:
        self.user = user

    def to_dict(self) -> Dict:
        return {
            "id": self.user.id,
            "name": self.user.name,
            "alias": self.user.alias,
            "avatar": Config.FILE_BASE_URL + self.user.avatar,
            "biography": self.user.biography,
            "createdAt": self.user.created_at,
            "updatedAt": self.user.updated_at
        }
