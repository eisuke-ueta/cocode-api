import json

from flask import Blueprint, jsonify, request

from app.commons.logger import Logger
from app.services.auth_service import AuthService
from app.services.file_service import FileService
from app.vos.file_vo import FileVo
from injector import inject

file_api = Blueprint('file_api', __name__)

logger = Logger(__name__)


@file_api.route('/files/upload', methods=["POST"])
@inject
def upload(file_service: FileService, auth_service: AuthService):
    try:
        auth = auth_service.validate(request.headers["Authorization"])
        if not auth:
            return jsonify({"message": "Not authorized"}), 401

        if not request.files:
            return jsonify({'message': 'Fail is not found ...'}), 400

        file_ = request.files.get('file')
        file_model = file_service.create(auth.user.id, file_)

        return jsonify({"file": FileVo(file_model).to_dict()}), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'Failed ...'}), 500
