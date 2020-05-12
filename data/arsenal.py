import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Arsenal(SqlAlchemyBase):
    __tablename__ = "arsenal"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    wtype = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    owned_by = sqlalchemy.Column(sqlalchemy.String)
    obtaining = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    orm.relation('User')
    orm.relation('Arsenal', back_populates="obtainingmethod")
