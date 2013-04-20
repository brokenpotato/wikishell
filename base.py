#-*- coding:utf-8 -*-

import tornado.web

from model import User

class BaseHandler(tornado.web.RequestHandler):
    @property
    def session(self):
        return self.application.session
    def write_error(self,status_code,**kwargs):
        if status_code in [403,404,500,503]:
            self.write('Error %s ', status_code)
        else:
            self.write('bad request')
    def get_current_user(self):
        auth=self.get_secure_cookie('auth')
        if not auth:
            return None
        query=self.session.query(User).filter_by(auth=auth)
        if query.count()==0:
            return None
        return query.one()
