import os

from dotenv import load_dotenv

load_dotenv(os.path.join(os.getcwd(), '.env'))


class Config:
    APP_NAME = os.getenv('APP_NAME', 'cocode')
    APP_DEBUG = os.getenv('APP_DEBUG', True)
    APP_HOST = os.getenv('APP_HOST', '127.0.0.1')
    APP_PORT = os.getenv('APP_PORT', '5000')
    SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{password}@{host}:{port}/{name}?charset=utf8'.format(
        **{
            'user': os.getenv('MYSQL_USER', 'admin'),
            'password': os.getenv('MYSQL_PASSWORD', ''),
            'host': os.getenv('MYSQL_HOST', 'cocode-mysql'),
            'port': os.getenv('MYSQL_PORT', '3306'),
            'name': os.getenv('MYSQL_DATABASE', 'cocode'),
        })
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False

    AWS_KEY = os.getenv('AWS_KEY', '')
    AWS_SECRET = os.getenv('AWS_SECRET', '')
    AWS_S3_REGION = os.getenv('AWS_S3_REGION', '')
    AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET', '')

    FILE_BASE_URL = "https://" + AWS_S3_BUCKET + ".s3-" + AWS_S3_REGION + ".amazonaws.com/"
