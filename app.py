import os
from . import create_app

app = create_app(os.getenv('FLASK_ENV') or 'default')
