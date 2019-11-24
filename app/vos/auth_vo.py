from typing import Dict

from app.models.auth import Auth


class AuthVo:
    def __init__(self, auth: Auth) -> None:
        self.auth = auth

    def to_dict(self) -> Dict:
        return {"token": self.auth.token, "email": self.auth.email}
