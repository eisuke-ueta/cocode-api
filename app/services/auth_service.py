from typing import Dict, Optional

import jwt
from app.commons.config import Config
from app.commons.exceptions import AuthNotValidException
from app.commons.logger import Logger
from app.models.auth import Auth
from app.repositories.auth_repository import AuthRepository
from flask_bcrypt import Bcrypt


class AuthService:

    HS256 = "HS256"
    UTF8 = "utf-8"

    def __init__(self, auth_repository: AuthRepository) -> None:
        self.logger = Logger(__name__)
        self.auth_repository = auth_repository
        self.bcrypt = Bcrypt()

    def login(self, fields: Dict, hash_passowrd: str) -> Optional[Auth]:
        email = fields["email"]
        password = fields["password"]

        # Check hashed password
        is_valid = self.bcrypt.check_password_hash(hash_passowrd, password)
        if not is_valid:
            raise AuthNotValidException("Not valid field values")

        token = self._encode_token(email, password)
        auth = self.auth_repository.find_by_token(token)
        if not auth:
            # Create token
            auth_fields = {"token": token, "email": email}
            auth = self.auth_repository.create(auth_fields)

        return auth

    def validate(self, authorization: str) -> Optional[Auth]:
        token = authorization.split()[1]
        auth = self.auth_repository.find_by_token(token)
        # TODO Check created_at
        return auth

    def create(self, fields: Dict) -> Optional[Auth]:
        auth_fields = {'token': fields['token'], 'email': fields['email']}
        auth = self.auth_repository.create(auth_fields)
        return auth

    def delete(self, id_: str) -> Optional[Auth]:
        auth = self.auth_repository.find(id_)
        if auth:
            self.auth_repository.delete(auth)
        return auth

    def _encode_token(self, email: str, password: str) -> str:
        payload = {'email': email, 'password': password}
        token = jwt.encode(payload, Config.APP_NAME, algorithm=self.HS256).decode(self.UTF8)
        return token

    def _decode_token(self, token: str) -> Dict:
        payload = jwt.decode(token.encode(self.UTF8), Config.APP_NAME, algorithm=self.HS256)
        return payload
