from flask import Flask
import os
from dotenv import load_dotenv
from utils import get_repo_list_from_csv
from flask_restful import Resource, Api

app = Flask(__name__)

API=Api(app)

from db import Github_Activities,db

def get_data():
    data=Github_Activities.query.all()
    return data

@app.route('/')
def index():
    print(get_data())
    return "Hello World"

@app.before_first_request
def startup():
    load_dotenv()
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
