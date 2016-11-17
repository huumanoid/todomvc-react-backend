from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()

DBSession = scoped_session(sessionmaker(autoflush=True, autocommit=False))


class TodoEntry(DeclarativeBase):
    __tablename__ = 'list'

    def __init__(self, title, completed):
        self.title = title
        self.completed = completed

    id = Column(Integer, primary_key=True)
    title = Column(String(256))
    completed = Column(Boolean, default=False)

class Model:
    TodoEntry = TodoEntry

    DBSession = DBSession
    metadata = DeclarativeBase.metadata

    def init_model(self, engine):
        self.DBSession.configure(bind=engine)
