import os
import tempfile
from datetime import datetime

import shortuuid


class FileHelper(object):

    def get_temporary_path(self, filename: str) -> str:
        directory = tempfile.mkdtemp()
        temporary_dir = os.path.join(directory, str(shortuuid.uuid()))
        os.makedirs(temporary_dir, exist_ok=True)

        temporary_path = os.path.join(temporary_dir, filename)
        return temporary_path
