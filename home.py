#-*- coding:utf-8 -*-
''' the home page after a user logged on'''

from base import BaseHandler

class HomeHandler(BaseHandler):
    pass


urls=[(r'/home', HomeHandler)]