import sys

from tg import expose, redirect, TGController, RestController
from tg import redirect, response
from wsgiref.simple_server import make_server

import appconfig
from model import TodoEntry, DBSession

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

class TodoController(RestController):

    @expose('json')
    def put(self, id, title, completed):
        todo = DBSession.query(TodoEntry).get(id)
        todo.title = title
        todo.completed = completed == 'true'
        DBSession.commit()

    @expose('json')
    def patch(self, id, title=None, completed=None):
        todo = DBSession.query(TodoEntry).get(id)
        todo.title = title if title != None else todo.title
        todo.completed = completed == 'true' if completed != None else todo.completed
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

config = appconfig.createConfig(minimal=True, root_controller=RootController())
application = config.make_wsgi_app()


print("Serving on port ", port, "...")
httpd = make_server('', port, application)
httpd.serve_forever()
