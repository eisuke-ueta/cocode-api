from flask import Flask
from flask_cors import CORS
from flask_injector import FlaskInjector, request

from app.apis.auth_api import auth_api
from app.apis.file_api import file_api
from app.apis.note_api import note_api
from app.apis.user_api import user_api
from app.commons.config import Config
from app.database import db, init_db
from app.repositories.auth_repository import AuthRepository
from app.repositories.file_repository import FileRepository
from app.repositories.note_repository import NoteRepository
from app.repositories.user_repository import UserRepository
from app.repositories.tag_repository import TagRepository
from app.services.auth_service import AuthService
from app.services.file_service import FileService
from app.services.note_service import NoteService
from app.services.user_service import UserService


def _create_app(config_mode='development'):
    app = Flask(Config.APP_NAME)
    app.config.from_object(Config)

    CORS(app)
    init_db(app)

    app.register_blueprint(user_api, url_prefix='/api/')
    app.register_blueprint(auth_api, url_prefix='/api/')
    app.register_blueprint(note_api, url_prefix='/api/')
    app.register_blueprint(file_api, url_prefix='/api/')

    FlaskInjector(app=app, modules=[_bind])

    return app


def _bind(binder):

    # Auth
    auth_repository = AuthRepository(db)
    auth_service = AuthService(auth_repository)
    binder.bind(AuthRepository, to=auth_repository, scope=request)
    binder.bind(AuthService, to=auth_service, scope=request)

    # File
    file_repository = FileRepository(db)
    file_service = FileService(file_repository)
    binder.bind(FileRepository, to=file_repository, scope=request)
    binder.bind(FileService, to=file_service, scope=request)

    # User
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    binder.bind(UserRepository, to=user_repository, scope=request)
    binder.bind(UserService, to=user_service, scope=request)

    # Tag
    tag_repository = TagRepository(db)
    binder.bind(TagRepository, to=tag_repository, scope=request)

    # Note
    note_repository = NoteRepository(db)
    note_service = NoteService(note_repository, tag_repository)
    binder.bind(NoteRepository, to=note_repository, scope=request)
    binder.bind(NoteService, to=note_service, scope=request)


app = _create_app()
