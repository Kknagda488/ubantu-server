from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()
from flask_migrate import Migrate

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from app.routes import home, job, testcase,auth 
with app.app_context():
    db.create_all() 