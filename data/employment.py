import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Employment(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'employment'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("users.id"))
    job = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    experience = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=False, nullable=True)
    start_time = sqlalchemy.Column(sqlalchemy.Time, nullable=True)
    end_time = sqlalchemy.Column(sqlalchemy.Time, nullable=True)
    user = sqlalchemy.Column(sqlalchemy.String, nullable=True)
