import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class ObtainingMethod(SqlAlchemyBase):
    __tablename__ = "obtaining"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    mtype = sqlalchemy.Column(sqlalchemy.String)
    method = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    relates_to = sqlalchemy.Column(sqlalchemy.String)

    orm.relation('Arsenal')