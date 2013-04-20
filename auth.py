#-*- coding:utf-8 -*-
'''
deal with the default page (/) , login(/login),logout(/logout) ,install page(/install) and error page(unhandled urls like /abcdefg)

'''
import hashlib
import datetime
import tornado.httpserver

from base import BaseHandler
from model import User

        
class ErrorHandler(BaseHandler):

    def get(self):
        raise tornado.web.HTTPError(404)
        
    def post(self):
        pass

class LoginHandler(BaseHandler):
    
    login_url=''
    default_url='/home'
    
    def setLoginUrl(self,url):
        self.login_url=url
    def prepare(self):
        self.setLoginUrl(self.request.full_url()) # get a url with 'next' argument
        
    def get(self):
        
        if self.current_user:
            self.redirect(self.default_url)
            return
        self.render('login.html',usr=None,error=0,login_url=self.login_url)
        
    def post(self):
        if self.current_user:
            return
        usr=self.get_argument('usr',default=None)
        pwd=self.get_argument('pwd',default=None)
        if not usr or not pwd:
            self.render('login.html',usr=usr,error=1,login_url=self.login_url)
            return
        auth=hashlib.sha1(str(usr)+str(pwd)+'lostandfound').hexdigest()
        query=self.session.query(User).filter_by(auth=auth)
        if query.count()==0:
            self.render('login.html',usr=usr,error=2,login_url=self.login_url)
            return
        self.set_secure_cookie('auth',auth,expires_days=21)# the cookie expires in 21 days
        try:
            next=self.get_argument('next')
            self.redirect(next)
            return            
        except:
            pass
        self.redirect(self.default_url)
        

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('auth')
        self.redirect('/')
    def post(self):
        pass

class RegisterHandler(BaseHandler):
    def get(self):
        self.render('register.html')
    def post(self):
        usr=self.get_argument('usr')
        pwd=self.get_argument('pwd')
        nickname=self.get_argument('nickname')
        if not usr or not pwd or not nickname:
            self.render('register.html',error=0)# can't be empty
            return
        user=self.session.query(User).filter(User.name==usr)
        if user.count()!=0:
            self.render('register.html',error=1)#user exists
            return
        auth=hashlib.sha1(str(usr)+str(pwd)+'lostandfound').hexdigest()
        user=User(usr,nickname,auth,datetime.datetime.now())
        self.session.add(user)
        self.session.commit()
        self.redirect('/login')
        

class InstallHandler(BaseHandler):
    def get(self):
        table=self.session.query(User)
        if table.count()!=0:
            raise tornado.web.HTTPError(404)
        self.render('install.html',usr=None,error=0)
    def post(self):
        name=self.get_argument('usr',default=None)
        pwd=self.get_argument('pwd',default=None)
        nickname=self.get_argument('nickname',default=None)
        if not usr or not pwd or not nickname :
            self.render('install.html',usr=usr,error=1)
        auth=hashlib.sha1(str(usr)+str(pwd)+'lostandfound').hexdigest()
        user=User(name,nickname,auth,datetime.now)
        self.session.add(user)
        self.session.commit()
        self.redirect('/login')
        
# ErrorHandler.urls must be at the end of all handler's urls
urls=[(r'/login',LoginHandler),
    (r'/logout',LogoutHandler),
    (r'/register',RegisterHandler),
    (r'/install',InstallHandler),
    (r'/(.*)',ErrorHandler)]
