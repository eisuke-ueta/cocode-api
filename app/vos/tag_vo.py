from typing import Dict

from app.models.tag import Tag


class TagVo:
    def __init__(self, tag: Tag) -> None:
        self.tag = tag

    def to_dict(self) -> Dict:
        return {"id": self.tag.id, "name": self.tag.name}
