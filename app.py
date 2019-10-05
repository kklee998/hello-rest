import os
from journal import create_app

app = create_app(os.getenv('FLASK_ENV') or 'default')
