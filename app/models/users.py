from sqlalchemy import Column, Integer, String, create_engine, Boolean, JSON
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash

from database import Base

#Base Model of Users object for mysql
class Users(Base):
    __tablename__ = "users"

    #Columns of the users table
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(128))
    username = Column(String(128))
    password_hashed = Column(String(255))
    hours_worked = Column(Integer, default=0)
    active = Column(JSON, default= "{\"active\": false, \"time_id\": null}")

    def __repr__(self):
        return f'Username: {self.username}'

    #hashing method for when registering a new user account
    def set_password_hash(self, password):
        self.password_hashed = generate_password_hash(password=password)

    #hash check for when the user is logging in
    def check_hashed_password(self, password: str) -> bool:
        return check_password_hash(pwhash=self.password_hashed, password=password)

