from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
import logging
from dotenv import load_dotenv
import os

db = SQLAlchemy()

load_dotenv()

SessionLocal = None

def init_db(app):
    global SessionLocal

    db.init_app(app)

    with app.app_context():
        SessionLocal = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=db.engine)
        )

def create_tables(app):
    with app.app_context():
        db.create_all()
        logging.info("Database tables created successfully.")

def get_session():
    return SessionLocal()
