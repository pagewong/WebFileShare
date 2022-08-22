# coding=utf-8
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from flask_app import create_app

if __name__ == '__main__':
    app = create_app()
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(app.config.get('PORT'), address=app.config.get('HOST'))
    IOLoop.instance().start()
