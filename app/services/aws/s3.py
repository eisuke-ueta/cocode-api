from datetime import datetime

import boto3
import shortuuid
from app.commons.config import Config


class S3(object):
    @staticmethod
    def _get_client():
        return boto3.client(
            's3',
            aws_access_key_id=Config.AWS_KEY,
            aws_secret_access_key=Config.AWS_SECRET,
            region_name=Config.AWS_S3_REGION)

    def create_file(self, filepath: str, media_type: str) -> str:
        key = self._generate_key()
        s3 = self._get_client()
        s3.upload_file(
            Filename=filepath,
            Bucket=Config.AWS_S3_BUCKET,
            Key=key,
            ExtraArgs={
                'ContentType': media_type,
                'ACL': 'public-read'
            })
        return key

    def _generate_key(self) -> str:
        return datetime.today().strftime('%Y%m%d') + str(shortuuid.uuid())
