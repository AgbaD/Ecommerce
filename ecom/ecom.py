#!/usr/bin/python3
# Author:   @AgbaD || @agba_dr3

from app import create_app, search
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    return dict(app=app)


def test():
    pass


if __name__ == "__main__":
    app.run()