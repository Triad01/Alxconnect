import os
from dotenv import load_dotenv

load_dotenv()


"""
ALXCONNECT CONFIGURATION FILE
"""


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')