from app.models.file import File
from app.repositories.base_repository import BaseRepository


class FileRepository(BaseRepository):
    model_class = File
