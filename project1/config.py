import os
base_dir=os.path.abspath(os.path.dirname(__file__)) 

 
class Config(object):
   SQLALCHEMY_DATABASE_URI='sqlite:///flaskpro.db'
 
   SQLALCHEMY_TRACK_MODIFICATIONS = False
   SECRET_KEY= os.environ.get('SECRET_KEY') or 'you will never know'
   GOOGLE_CLIENT_ID = '819086855144-npbcbc1ae0avldug56hh5a4juq8n7hpn.apps.googleusercontent.com'
   GOOGLE_CLIENT_SECRET = 'zovxbInUxgEsDpklMF055jiJ' 
   REDIRECT_URI = '//127.0.0.1:5000/callback/google'  
   

   OAUTH_CREDENTIALS={
        'google': {
            'id': GOOGLE_CLIENT_ID,
            'secret': GOOGLE_CLIENT_SECRET
        }
   }

