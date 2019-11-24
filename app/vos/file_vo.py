from typing import Dict

from app.commons.config import Config
from app.models.file import File


class FileVo:
    def __init__(self, file: File) -> None:
        self.file = file

    def to_dict(self) -> Dict:
        return {
            "id": self.file.id,
            "userId": self.file.user_id,
            "path": Config.FILE_BASE_URL + self.file.path,
            "name": self.file.name,
            "media_type": self.file.media_type,
            "size": self.file.size,
            "createdAt": self.file.created_at,
            "updatedAt": self.file.updated_at
        }
