import os

from flask import Flask, render_template
from flask_pymongo import PyMongo
from pymongo import MongoClient

from get_predict import buy_or_sell

#app = Flask(__name__)    
#app.config["MONGO_URI"] = "mongodb://localhost:27017/finance"
#mongo = PyMongo(app)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
    
    #app.config["MONGO_URI"] = "mongodb://localhost:27017/finance"
    #mongo = PyMongo(app)
    client = MongoClient()
    db = client.finance
    AAPL_collection = db.AAPL
    AMZN_collection = db.AMZN
    FB_collection = db.FB
    GOOGL_collection = db.GOOGL
    MSFT_collection = db.MSFT
    NFLX_collection = db.NFLX

    

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    

    def hello():
        buy_or_sell()
        #return render_template('hello.html', message="coucou")
        return render_template('hello.html')


    return app
    
    
    
    @app.route('/')
    def function():
        buy_or_sell()
    
    
#    def get_my_cols():
 #   client = MongoClient()
  #  db = client.finance
   # AAPL_collection = db.AAPL_col

    
    

