import os
from flask import Flask
from flask_migrate import Migrate

from .models import db

# # import pdb; pdb.set_trace()
# database = os.path.join(BASE_DIR, "database.db")
app = Flask(__name__)
FLASK_CONFIGURATION = os.getenv('FLASK_CONFIGURATION', 'settings/local.py')
app.config.from_pyfile(FLASK_CONFIGURATION)
if FLASK_CONFIGURATION == 'settings/local.py':
    from flask_debugtoolbar import DebugToolbarExtension
    DebugToolbarExtension(app)

db.init_app(app)
migrate = Migrate(app, db)


def create_tables():
    #     # db.create_all(app)
    with app.app_context():
        db.create_all()


from .import views

views.login_manager.init_app(app)
