from tg import expose, redirect, TGController, AppConfig, RestController
from tg import redirect, response
from wsgiref.simple_server import make_server

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import logging

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

class TodoController(RestController):

    @expose('json')
    def put(self, id, title, completed):
        todo = DBSession.query(TodoEntry).get(id)
        todo.title = title
        todo.completed = completed == 'true'
        DBSession.commit()

    @expose('json')
    def post(self, title, completed=None):
        todo = TodoEntry(title=title, completed=completed)
        DBSession.add(todo)
        DBSession.commit()
        return { 'response': { 'id': todo.id }}


    @expose('json')
    def post_delete(self, id):
        todo = DBSession.query(TodoEntry).get(id)

        if todo == None:
            response.status = 404
            return

        DBSession.delete(todo)
        DBSession.commit()

    @expose('json')
    def get_one(self, id):
        todo = DBSession.query(TodoEntry).get(id)

        if todo == None:
            response.status = 404
            return

        return dict(response={ 'todo': todo })

    @expose('json')
    def get_all(self):
        todos = DBSession.query(TodoEntry).all()
        return { 'response': { 'todos': todos } }

class RootController(TGController):
    todos = TodoController()

    @expose()
    def index(self):
        redirect('/index.html')

config = AppConfig(minimal=True, root_controller=RootController())

config.use_sqlalchemy = True
config['sqlalchemy.url'] = 'mysql://_ru_hmnid_tstusr:password@localhost/_ru_hmnid_testdb'
config.model = Model()
config.serve_static = True
config.paths['static_files'] = 'todomvc/examples/react'

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

application = config.make_wsgi_app()


print("Serving on port 8080...")
httpd = make_server('', 8080, application)
httpd.serve_forever()
