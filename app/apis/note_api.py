import json

from flask import Blueprint, jsonify, request

from app.commons.logger import Logger
from app.helpers.string_helper import StringHelper
from app.models.note import Note
from app.services.auth_service import AuthService
from app.services.note_service import NoteService
from app.vos.note_vo import NoteVo
from injector import inject

note_api = Blueprint('note_api', __name__)

logger = Logger(__name__)


@note_api.route('/notes', methods=["GET"])
@inject
def index(note_service: NoteService):
    try:
        offset = request.args.get('offset', default=0, type=int)
        limit = request.args.get('limit', default=10, type=int)
        status = request.args.get('status', default=Note.STATUS_PUBLISHED, type=str)
        user_id = request.args.get('userId', default=None, type=str)
        keyword = request.args.get('keyword', default=None, type=str)

        note_models = note_service.get(offset=offset, limit=limit, user_id=user_id, status=status, keyword=keyword)
        notes = [NoteVo(note_model).to_dict() for note_model in note_models]

        return jsonify({"notes": notes}), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'Failed ...'}), 500


@note_api.route('/notes/count', methods=["GET"])
@inject
def count(note_service: NoteService):
    try:
        status = request.args.get('status', default=Note.STATUS_PUBLISHED, type=str)
        user_id = request.args.get('userId', default=None, type=str)
        keyword = request.args.get('keyword', default=None, type=str)

        count = note_service.count(user_id=user_id, status=status, keyword=keyword)

        return jsonify({"count": count}), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'Failed ...'}), 500


@note_api.route('/notes/create', methods=["POST"])
@inject
def create(note_service: NoteService, auth_service: AuthService):
    try:
        auth = auth_service.validate(request.headers["Authorization"])
        if not auth:
            return jsonify({"message": "Not authorized"}), 401

        fields = json.loads(request.form["fields"])
        logger.error(fields["tags"])
        logger.error(type(fields["tags"]))
        fields = _convert_to_snake_case(fields)

        note = note_service.create(fields)

        return jsonify({"note": NoteVo(note).to_dict()}), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'Failed ...'}), 500


@note_api.route('/notes/update', methods=["POST"])
@inject
def update(note_service: NoteService, auth_service: AuthService):
    try:
        auth = auth_service.validate(request.headers["Authorization"])
        if not auth:
            return jsonify({"message": "Not authorized"}), 401

        fields = json.loads(request.form["fields"])
        logger.error(fields["tags"])
        logger.error(type(fields["tags"]))
        fields = _convert_to_snake_case(fields)

        note = note_service.update(fields)

        return jsonify({"note": NoteVo(note).to_dict()}), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'Failed ...'}), 500


@note_api.route('/notes/<string:id>', methods=["GET"])
@inject
def get(id: str, note_service: NoteService):
    try:
        note = note_service.find(id)
        return jsonify({"note": NoteVo(note).to_dict()}), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'Failed ...'}), 500


@note_api.route('/notes/delete/<string:id>', methods=["DELETE"])
@inject
def delete(id: str, note_service: NoteService, auth_service: AuthService):
    try:
        auth = auth_service.validate(request.headers["Authorization"])
        if not auth:
            return jsonify({"message": "Not authorized"}), 401

        note_model = note_service.delete(id)
        note = NoteVo(note_model).to_dict() if note_model else {}
        return jsonify({"note": note}), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'Failed ...'}), 500


def _convert_to_snake_case(fields: dict) -> dict:
    new_fields = {}
    for key, value in fields.items():
        new_key = StringHelper().to_snake_case(key)
        new_fields[new_key] = value
    return new_fields
