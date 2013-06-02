#-*- coding:utf-8 -*-


from base import BaseHandler

'''a handler to deal with the search request'''

class SearchHandler(BaseHandler):
    def get(self):
        wd=self.get_argument('wd')
        self.write('you searched %s' %wd)
    def post(self):
        pass

urls=[(r'/s',SearchHandler)]
