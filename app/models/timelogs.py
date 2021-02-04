from sqlalchemy import Column, Integer, String, create_engine, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from werkzeug.security import generate_password_hash, check_password_hash

from database import Base


#Base Model of timelogss object for mysql
class timelogs(Base):
    __tablename__ = "timelogs"

    #timelogs table columns
    time_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    time_start = Column(DateTime)
    time_stop = Column(DateTime)
    hours_shift = Column(Integer)
    relation = relationship("Users")
