from sqlalchemy import Column,Integer,String,DateTime,ForeignKey
from sqlalchemy.orm import relationship

from flask_login import UserMixin
from newflask import login, db
from newflask.base import engine
from wtforms.validators import ValidationError
from flask import url_for, current_app, redirect, request
from rauth import OAuth2Service 
import json, urllib
from urllib.request import urlopen




class User(UserMixin, db.Model):
    __tablename__ ='user'
    id=Column(Integer,primary_key=True)
    name=Column(String(10),index=True )
    username=Column(String(10),index=True , unique=True)
    email=Column(String(120),index=True , unique=True)
    accntno=Column(String(10), index=True, unique=True)
    ifsccode=Column(String(10), index=True)
    password=Column(String(20))
    payment_type=Column(String(10))
    transaction_type=Column(String(10))
    usertype=Column(String(10),default="USER")
    blogs = relationship('Blog', backref='author' ,cascade="all, delete-orphan" ,lazy='dynamic')
    def __repr__(self):
        return '<User {}>'.format(self.username)
   
    def __init__(self, name  ,username ,email ,password ,accntno ,ifsccode ,payment_type ,transaction_type,usertype):
        self.name=name
        self.username=username
        self.email=email
        self.password=password
        self.accntno=accntno
        self.ifsccode=ifsccode 
        self.payment_type=payment_type
        self.transaction_type=transaction_type
        self.usertype=usertype

class Blog(UserMixin,db.Model):
    __tablename__ ='blog'
    id = Column(Integer, primary_key=True)
    title=Column(String(30),index=True )
    message=Column(String(140))
    user_id = Column(Integer, ForeignKey('user.id'))
    

    def __repr__(self):
        return '<Post {}>'.format(self.title)
    
    def __init__(self ,message  ,user_id ,title):
        self.message=message
        self.user_id=user_id
        self.title=title

class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.provider_name,
                        _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers={}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]

class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super(GoogleSignIn, self).__init__('google')
        googleinfo = urlopen('https://accounts.google.com/.well-known/openid-configuration')
        google_params = json.load(googleinfo)
        self.service = OAuth2Service(
                name='google',
                client_id=self.consumer_id,
                client_secret=self.consumer_secret,
                authorize_url=google_params.get('authorization_endpoint'),
                base_url=google_params.get('userinfo_endpoint'),
                access_token_url=google_params.get('token_endpoint')
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
            )

    def callback(self):
        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
                data={'code': request.args['code'],
                      'grant_type': 'authorization_code',
                      'redirect_uri': self.get_callback_url()},
                decoder = json.loads
        )
        me = oauth_session.get('').json()
        return ( 
                 me [ name],
                  me [email])
        