from operator import and_
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from datetime import date, datetime

# from utils import get_repo_list_from_csv
from flask_restful import Resource, Api
from sqlalchemy import and_, func


app = Flask(__name__)

api = Api(app)

from db import Github_Activities, db


class User_Stats(Resource):

    # return count of commits and pull requests for a user
    def get(self, user_id):
        user_id = int(user_id)
        today = date.isoformat(date.today())
        commits = Github_Activities.query.filter(
            and_(
                Github_Activities.author_id == user_id,
                Github_Activities.type == "commit",
                Github_Activities.created_at >= today,
            )
        ).count()
        pull_requests = Github_Activities.query.filter(
            and_(
                Github_Activities.author_id == user_id,
                Github_Activities.type == "pull_request",
                Github_Activities.created_at >= today,
            )
        ).count()
        return jsonify(
            {
                "date": today,
                "user_id": user_id,
                "commits": commits,
                "pull_requests": pull_requests,
            }
        )


class Repo_Stats(Resource):

    # return count of commits and pull requests for a repo
    def get(self, repo_owner, repo_name):
        repo_name = repo_owner + "/" + repo_name
        today = date.isoformat(date.today())
        commits = Github_Activities.query.filter(
            and_(
                Github_Activities.repo_name == repo_name,
                Github_Activities.type == "commit",
                Github_Activities.created_at >= today,
            )
        ).count()
        pull_requests = Github_Activities.query.filter(
            and_(
                Github_Activities.repo_name == repo_name,
                Github_Activities.type == "pull_request",
                Github_Activities.created_at >= today,
            )
        ).count()
        return jsonify(
            {
                "date": today,
                "repo_name": repo_name,
                "commits": commits,
                "pull_requests": pull_requests,
            }
        )


api.add_resource(User_Stats, "/github/user/stats/<string:user_id>")
api.add_resource(
    Repo_Stats, "/github/repo/stats/<string:repo_owner>/<string:repo_name>"
)


@app.route("/")
def index():
    return "Hello World"


@app.before_first_request
def startup():
    load_dotenv()
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
