import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


#creating the sql objects and sessions, as well as Base for the table objects
db = SQLAlchemy()
engine = create_engine('mysql://root:root@db/timesheetlog', pool_size=20, max_overflow=0)
Base = declarative_base()
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base.query = db.session.query_property()


#Class for initiating the database, engine, session, and query base.
class Database():

    def __init__(self):
        self.db = db
        self.engine = engine
        self.Base = Base
        self.db_session = db_session

    #Haven't utilized this method from the database class
    def read_user_table(self):
        with engine.connect() as connection:
            result = connection.execute("SELECT * from users")
            for row in result:
                print(row)
            return result


    # probably not the proper place to insert the method
    # def save_to_database(self):
    #     with engine.connect as connection:
    #         select = self.read_database()
    #         query = connection.execute(f"insert into users (email, username, password) values ('user2@gmail.com','user2','password2')")
    #         print(query.values)
    #         return query

