import os

BASE_DIR = os.path.dirname(os.path.abspath(__name__))
database = os.path.join(BASE_DIR, "database.db")

SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(database)
SECRET_KEY = 'hello'
