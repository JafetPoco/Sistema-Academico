from flask_sqlalchemy import SQLAlchemy
import logging
from dotenv import load_dotenv
import os

db = SQLAlchemy()

load_dotenv()

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

def init_db(app):
    db.init_app(app)

def create_tables(app):
    with app.app_context():
        db.create_all()
        logging.info("Database tables created successfully.")