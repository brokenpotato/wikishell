#-*- coding:utf-8 -*-

from base import BaseHandler


class MainHandler(BaseHandler):
	def get(self):
		self.render('index.html')
	def post(self):
		pass

urls=[(r'/',MainHandler),]
