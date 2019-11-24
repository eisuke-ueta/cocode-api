import os
import shutil
from typing import List, Optional

from werkzeug import FileStorage, secure_filename

from app.commons.logger import Logger
from app.helpers.file_helper import FileHelper
from app.models.file import File
from app.repositories.file_repository import FileRepository
from app.services.aws.s3 import S3


class FileService:
    def __init__(self, file_repository: FileRepository) -> None:
        self.logger = Logger(__name__)
        self.file_repository = file_repository

    def get(self, offset: int, limit: int) -> List[File]:
        return self.file_repository.get(offset, limit, File.created_at.desc())

    def find(self, id: str) -> Optional[File]:
        return self.file_repository.find(id)

    def create(self, user_id: str, file_: FileStorage) -> Optional[File]:
        # Save file in local
        filename = secure_filename(file_.filename)
        temporary_path = FileHelper().get_temporary_path(filename)
        file_.save(temporary_path)

        # Update file to S3
        path = S3().create_file(temporary_path, file_.content_type)

        fields = {
            'user_id': user_id,
            'name': filename,
            'media_type': file_.content_type,
            'path': path,
            'size': os.path.getsize(temporary_path)
        }
        file_model = self.file_repository.create(fields)

        # Delete directory
        shutil.rmtree(os.path.dirname(temporary_path))

        return file_model

    def delete(self, id: str) -> Optional[File]:
        delete_file = self.file_repository.find(id)
        if delete_file:
            self.file_repository.delete(delete_file)
        return delete_file
