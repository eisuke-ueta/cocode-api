import json

from flask import Blueprint, jsonify, request

from app.commons.logger import Logger
from app.services.auth_service import AuthService
from app.services.file_service import FileService
from app.services.user_service import UserService
from app.vos.user_vo import UserVo
from injector import inject

user_api = Blueprint('user_api', __name__)

logger = Logger(__name__)


@user_api.route('/users', methods=["GET"])
@inject
def index(user_service: UserService):
    try:
        offset = request.args.get('offset', default=0, type=int)
        limit = request.args.get('limit', default=10, type=int)

        user_models = user_service.get(offset, limit)
        users = [UserVo(user_model).to_dict() for user_model in user_models]

        return jsonify({"users": users}), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'Failed ...'}), 500


@user_api.route('/users/update', methods=["POST"])
@inject
def update(user_service: UserService, file_service: FileService, auth_service: AuthService):
    try:
        auth = auth_service.validate(request.headers["Authorization"])
        if not auth:
            return jsonify({"message": "Not authorized"}), 401

        fields = json.loads(request.form["fields"])

        if request.files:
            file_ = request.files.get('file')
            file_model = file_service.create(fields["id"], file_)
            fields["avatar"] = file_model.path

        user = user_service.update(fields)

        return jsonify({"user": UserVo(user).to_dict()}), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'Failed ...'}), 500


@user_api.route('/users/<string:id>', methods=["GET"])
@inject
def get(id: str, user_service: UserService):
    try:
        user = user_service.find(id)
        return jsonify({"user": UserVo(user).to_dict()}), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'Failed ...'}), 500


@user_api.route('/users/alias/<string:alias>', methods=["GET"])
@inject
def get_by_alias(alias: str, user_service: UserService):
    try:
        user = user_service.find_by_alias(alias)
        return jsonify({"user": UserVo(user).to_dict()}), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'Failed ...'}), 500


@user_api.route('/users/delete/<string:id>', methods=["DELETE"])
@inject
def delete(id: str, user_service: UserService, auth_service: AuthService):
    try:
        auth = auth_service.validate(request.headers["Authorization"])
        if not auth:
            return jsonify({"message": "Not authorized"}), 401

        user = user_service.delete(id)
        return jsonify({"user": UserVo(user).to_dict()}), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'Failed ...'}), 500
