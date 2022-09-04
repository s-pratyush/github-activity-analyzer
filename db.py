from contextlib import nullcontext
from flask_sqlalchemy import SQLAlchemy
from main import app
import os

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
db = SQLAlchemy(app)

class Github_Activities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repo_name = db.Column(db.String(80), unique=True, nullable=False)
    type = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer,nullable=False)
    activity_id = db.Column(db.Integer,nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Github_Activity %r>' % str(self.id)