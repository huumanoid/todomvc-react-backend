from tg import expose, TGController, AppConfig, RestController
from wsgiref.simple_server import make_server

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()

DBSession = scoped_session(sessionmaker(autoflush=True, autocommit=False))


class TodoEntry(DeclarativeBase):
    __tablename__ = 'list'

    def __init__(self, content, active):
        self.content = content
        self.active = active

    id = Column(Integer, primary_key=True)
    content = Column(String(256))
    active = Column(Integer, default=True)

class Model:
    TodoEntry = TodoEntry

    DBSession = DBSession
    metadata = DeclarativeBase.metadata

    def init_model(self, engine):
        self.DBSession.configure(bind=engine)

class TodoController(RestController):

    @expose('json')
    def put(self, content):
        return 'todo ' + content + ' has been put\r\n'

    @expose('json')
    def post(self, content='stub', active=None):
        DBSession.add(TodoEntry(content=content, active=active))
        DBSession.commit()
        return

    @expose('json')
    def post_delete(self, id):
        DBSession.query(TodoEntry).filter(TodoEntry.id==id).delete()
        DBSession.commit()
        return 'todo ' + id + ' has been deleted\r\n'

    @expose('json')
    def get_one(self, id):
        return 'todo: ' + id + '\r\n'

    @expose('json')
    def get_all(self):
        todos = DBSession.query(TodoEntry).all()
        return dict(list=todos)

class RootController(TGController):
    todo = TodoController()

    @expose()
    def index(self):
        return 'Hello World\r\n'

config = AppConfig(minimal=True, root_controller=RootController())

config.use_sqlalchemy = True
config['sqlalchemy.url'] = 'mysql://_ru_hmnid_tstusr:password@localhost/_ru_hmnid_testdb'
config.model = Model()

application = config.make_wsgi_app()


print("Serving on port 8080...")
httpd = make_server('', 8080, application)
httpd.serve_forever()
