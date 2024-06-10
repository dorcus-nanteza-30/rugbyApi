from flask import Flask
from app.extensions import db

def create_app():

     app =  Flask(__name__)


     db.init_app(app)

     @app.route("/") 
     def home():
         return "Website Api"


     return app 

 
