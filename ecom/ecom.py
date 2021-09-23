#!usr/bin/python3
# Author:   @AgbaD || @agba_dr3

import os
from dotenv import load_dotenv
from app import db, create_app
from flask_migrate import Migrate
from app.models import Merchant, Store, Product, Category, Feedback, User

load_dotenv()

app = create_app(os.getenv('CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, app=app)


if __name__ == "__main__":
    app.run()
