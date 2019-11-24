import copy
import json

from flask import Blueprint, jsonify, request

from app.commons.logger import Logger
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.vos.auth_vo import AuthVo
from app.vos.user_vo import UserVo
from injector import inject

logger = Logger(__name__)
auth_api = Blueprint('auth_api', __name__)


@auth_api.route('/signup', methods=["POST"])
@inject
def signup(auth_service: AuthService, user_service: UserService):
    try:
        form = json.loads(request.data.decode('utf-8'))

        user = user_service.create(copy.deepcopy(form))
        auth = auth_service.login(copy.deepcopy(form), user.password)

        return jsonify({"auth": AuthVo(auth).to_dict(), "user": UserVo(user).to_dict()}), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'Failed ...'}), 500


@auth_api.route('/login', methods=["POST"])
@inject
def login(auth_service: AuthService, user_service: UserService):
    try:
        form = json.loads(request.data.decode('utf-8'))

        user = user_service.find_by_email(form["email"])
        if not user:
            return jsonify({"message": "User is not found."}), 400
        auth = auth_service.login(form, user.password)

        return jsonify({"auth": AuthVo(auth).to_dict(), "user": UserVo(user).to_dict()}), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'Failed ...'}), 500


@auth_api.route('/signin', methods=["POST"])
@inject
def signin(auth_service: AuthService, user_serivce: UserService):
    try:
        auth = auth_service.validate(request.headers["Authorization"])
        if not auth:
            return jsonify({"message": "Not authorized"}), 401

        return jsonify({"auth": AuthVo(auth).to_dict(), "user": UserVo(auth.user).to_dict()}), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'Failed ...'}), 500


@auth_api.route('/logout', methods=["DELETE"])
@inject
def logout(auth_service: AuthService):
    try:
        auth = auth_service.validate(request.headers["Authorization"])
        if not auth:
            return jsonify({"message": "Not authorized"}), 401

        auth = auth_service.delete(auth.id)

        return jsonify({"auth": AuthVo(auth).to_dict()}), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'Failed ...'}), 500
