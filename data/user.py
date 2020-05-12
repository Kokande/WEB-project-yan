import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)