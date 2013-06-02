#-*- coding:utf-8 -*-
'''
    the index file of the application. use 'python index.py' to launch the application'''

import os.path
import tornado.web
import tornado.ioloop
from tornado.options import define, options

from model import createSession
from home import urls as homeurls
from auth import urls as authurls
from main import urls as mainurls
from search import urls as searchurls

define('port', default=8888, help='run on the given port', type=int)


class Application(tornado.web.Application):

    def __init__(self):
        handlers=homeurls+mainurls+searchurls+authurls
        settings=dict(
        cookie_secret='icreatedausefulwikiofshellcommands',
        template_path=os.path.join(os.path.dirname(__file__), 'template'),
        static_path=os.path.join(os.path.dirname(__file__), 'static'),
        login_url='/login',
        xsrf_cookies=True,
        autoescape='xhtml_escape',
        site_title='WikiShell'
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.session=createSession()


def main():
    tornado.options.parse_command_line()
    app=Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__=='__main__':
    main()
