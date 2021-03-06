#-*- coding:utf-8 -*-

from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base #declared_attr
import datetime

from config import *

connectionString="mysql://%s:%s@%s:%s/%s?charset=utf8" %(MYSQL_USER, \
                    MYSQL_PASS, MYSQL_HOST, str(MYSQL_PORT), MYSQL_DB)

engine=create_engine(connectionString,echo=True,\
                    encoding='utf8',convert_unicode=True)
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
''' end of class User'''

class Shell(Base):
    __tablename__='shell'
    id=Column(Integer,primary_key=True)
    shell=Column(String(100))
    description=Column(String(200))
    arg=relationship('Arg')
    usage=relationship('Usage')
    platform=Column(String(20))
    #created=Column(DateTime,dafault=datetime.datetime.now())
    #creator=relationship('User',backref='wiki')

    def __init__(self,shell,des):
        self.shell=shell
        self.description=des
    def __repr__(self):
        return 'WiKi<%s,)%s>' %(self.shell,self.description)
'''end of class Shell'''

class Arg(Base):
    __tablename__='arg'
    id=Column(Integer,primary_key=True)
    arg=Column(String(10))
    description=Column(String(100))
    shell_id=Column(Integer,ForeignKey('shell.id'))

    def __init__(self,arg,des,shell_id):
        self.arg=arg
        self.description=des
        self.shell_id=shell_id

    def __repr__(self):
        return 'Arg<%s,%s>' %(self.arg,self.description)
''' end of class Arg'''

class Usage(Base):
    __tablename__='usage'
    id=Column(Integer,primary_key=True)
    usage=Column(String(50))
    description=Column(String(100))
    shell_id=Column(Integer,ForeignKey('shell.id'))

    def __init__(self,usage,des,shell_id):
        self.usage=usage
        self.description=des
        self.shell_id=shell_id
    def __repr__(self):
        return 'Usage<%s,%s>' %(self.usage,self.description)
''' end of class Usage '''

Base.metadata.create_all(engine)

def createSession():
    Session=sessionmaker(bind=engine)
    session=Session()
    return session
'''end of method createSession'''



