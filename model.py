#-*- coding:utf-8 -*-

from sqlalchemy.orm import sessionmaker,relationship,backref
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base,declared_attr
import datetime

from config import *

connectionString="mysql://%s:%s@%s:%s/%s?charset=utf8" \
                    %(MYSQL_USER,MYSQL_PASS,MYSQL_PORT,str(MYSQL_PORT),MYSQL_DB)

engine=create_engine(connectionString,echo=True,encoding='utf8',convert_unicode=True)
Base=declarative_base()

class User(Base):
    __tablename__='user'
    #__table_args__={'mysql_engine':'InnoDB'}
    id=Column(Integer,primary_key=True)
    name=Column(String(40),nullable=False,unique=True) # name should be an email address
    auth=Column(String(50),nullable=False,unique=True)
    nick=Column(String(30),nullable=False,unique=True)
    created=Column(DateTime,nullable=False,default=datetime.datetime.now())
    updated=Column(DateTime,nullable=False,default=datetime.datetime.now())
    
    def __init__(self,name,auth,nick):
        self.name=name
        self.auth=auth
        self.nick=nick
    def __repr__(self):
        return 'User<%s,%s>' %(self.nick,self.name)
class WiKi(Base):
    __tablename__='wiki'
    id=Column(Integer,primary_key=True)
    cmd=Column(String(100))
    des=Column(String(200))
    example=Column(String(200))
    parent=Column(Integer,default=0)
    platform=Column(String(20))
    created=Column(DateTime,dafault=datetime.datetime.now())
    creator=relationship('User',backref='wiki')
    
    def __init__(self,cmd,des,parent=0):
        self.cmd=cmd
        self.des=des
        self.parent=parent
    def __repr__(self):
        return 'WiKi<%s,%s>' %(self.cmd,self.des)


def createSession():
    Session=sessionmaker(bind=engine)
    session=Session()
    return session
    



