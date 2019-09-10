import os
import click
from app import create_app, db
from flask_migrate import Migrate
from app.models import User

app = create_app('Dev1')
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run()

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)
