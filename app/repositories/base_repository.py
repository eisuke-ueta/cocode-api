from typing import Any, Dict, List, Union

import shortuuid
from app.database import db
from flask_sqlalchemy import SQLAlchemy


class BaseRepository(object):
    model_class = db.Model

    def __init__(self, db: SQLAlchemy) -> None:
        self.session = db.session

    def all(self) -> List[db.Model]:
        return self.model_class.all()

    def get(self, offset: int, limit: int, order: Any = None) -> List[db.Model]:
        query = self.model_class.query
        if order is not None:
            query = query.order_by(order)

        return query.offset(offset).limit(limit).all()

    def create(self, fields: Dict) -> db.Model:
        id_ = str(shortuuid.uuid())
        while self.exist(id_):
            id_ = str(shortuuid.uuid())
        fields['id'] = id_

        model = self.model_class(**fields)
        self.session.add(model)
        self.session.commit()
        return model

    def update(self, model: db.Model, fields: Dict) -> db.Model:
        for key in fields:
            setattr(model, key, fields[key])
        self.session.add(model)
        self.session.commit()
        return model

    def delete(self, model: db.Model) -> bool:
        self.session.delete(model)
        self.session.commit()
        return True

    def find(self, primary_id: Any) -> db.Model:
        return self.model_class.query.filter_by(id=primary_id).first()

    def exist(self, primary_id: Union[int, str]) -> bool:
        return bool(self.model_class.query.filter_by(id=primary_id).first())
