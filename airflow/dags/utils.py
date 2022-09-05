import pandas as pd
import requests
import os
from dotenv import load_dotenv
import json
import psycopg2

load_dotenv()

conn = psycopg2.connect(
    host="localhost", database="test", user="test", password="test", port="5432"
)


def check_if_data_exists(id, type):
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM github__activities WHERE activity_id=%s AND type=%s", (id, type)
    )
    rows = cur.fetchone()
    if rows:
        return True
    else:
        return False


def get_repo_list_from_csv():
    try:
        df = pd.read_csv("repo.csv")
        repos = []
        for index, row in df.iterrows():
            repos.append([row["repo_name"], row["owner"]])
        return repos
    except Exception as e:
        print(e)
        print("Unable to read csv file")


def collect_repo_data():
    repos = get_repo_list_from_csv()
    BASEURL = "https://api.github.com/repos/"
    curr = conn.cursor()
    for repo in repos:

        token = os.getenv("GH_TOKEN")
        header = {"Authorization": "Bearer " + token}

        try:
            # get commits
            commit_url = BASEURL + repo[0] + "/commits"
            print(commit_url)
            r = requests.get(commit_url, headers=header)
            if r.status_code == 200:
                for commit in r.json():
                    if check_if_data_exists(commit["sha"], "commit"):
                        break
                    try:
                        curr.execute(
                            "INSERT INTO github__activities (repo_name,type,author_id,activity_id,created_at) VALUES (%s,%s,%s,%s,%s)",
                            (
                                repo[0],
                                "commit",
                                commit["author"]["id"],
                                commit["sha"],
                                commit["commit"]["author"]["date"],
                            ),
                        )
                        conn.commit()
                    except Exception as e:
                        conn.rollback()
                        print(e)
                        print(r[0], commit["sha"])
                        print("Skipped")
            else:
                print(commit_url, r.status_code)
        except Exception as e:
            print(e)
            print("Error in fetching commits")
            print(commit_url, r.status_code)

        # get pull requests
        try:
            pr_url = BASEURL + repo[0] + "/pulls"
            print(pr_url)
            r = requests.get(pr_url, headers=header)
            if r.status_code == 200:
                for pr in r.json():
                    if check_if_data_exists(str(pr["id"]), "pull_request"):
                        break
                    try:
                        curr.execute(
                            "INSERT INTO github__activities (repo_name,type,author_id,activity_id,created_at) VALUES (%s,%s,%s,%s,%s)",
                            (
                                repo[0],
                                "pull_request",
                                pr["user"]["id"],
                                pr["id"],
                                pr["created_at"],
                            ),
                        )
                        conn.commit()
                    except Exception as e:
                        conn.rollback()
                        print(e)
                        print(r[0], pr["id"])
                        print("Skipped")
            else:
                print(pr_url, r.status_code)
        except Exception as e:
            print(e)
            print("Error in fetching pull requests")
            print(pr_url, r.status_code)

    return "Data collected successfully"


collect_repo_data()


# from airflow import DAG
# from airflow.operators.dummy_operator import DummyOperator
# from airflow.operators.python_operator import PythonOperator
# from datetime import datetime, timedelta

# def print_hello():
#     # collect_repo_data()
#     return "function called"

# default_args = {
#     "owner": "airflow",
#     "depends_on_past": False,
#     "start_date": datetime.now(),
#     "email": ["airflow@example.com"],
#     "email_on_failure": False,
#     "email_on_retry": False,
#     "retries": 1,
#     "retry_delay": timedelta(minutes=5),
# }

# dag = DAG(
#     "hello_world",
#     description="Simple tutorial DAG",
#     schedule_interval="0 12 * * *",
#     default_args=default_args,
#     catchup=False,
# )


# t1 = DummyOperator(task_id="dummy_task", retries=3, dag=dag)

# t2 = PythonOperator(task_id="hello_task", python_callable=print_hello, dag=dag)

# # sets downstream foe t1
# t1 >> t2
