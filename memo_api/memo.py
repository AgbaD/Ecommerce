#!/usr/bin/python3
# Author:   @AgbaD | @agba_dr3

from app import db, create_app
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, app=app)


if __name__ == "__main__":
    app.run(debug=True)
