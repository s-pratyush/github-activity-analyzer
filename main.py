from flask import Flask, jsonify
from sqlalchemy import create_engine
import requests
import os
from dotenv import load_dotenv
from utils import get_repo_list_from_csv

app = Flask(__name__)

# conect to psql database

def connect_to_db():
    try:
        conn = create_engine("postgresql://test:test@localhost:5432/test")
        resp=conn.execute("SELECT now()")
        # print(resp)
        return conn
    except Exception as e:
        print(e)
        print("Unable to connect the database")

def collect_repo_data():
    repos=get_repo_list_from_csv()
    BASEURL="https://api.github.com/repos/"
    for repo in repos:
        try:
            token=os.getenv("GH_TOKEN")
            header={"Authorization":"Bearer "+token}
            url=BASEURL+repo[0]
            r=requests.get(url,headers=header)
            if r.status_code==200:
                return r.json()
            else:
                print(r.content,url,r.status_code)
        except Exception as e:
            print(e)
            print("Unable to fetch data")



@app.route('/')
def index():
    collect_repo_data()
    return jsonify({'message': 'Hello World!'})






if __name__ == '__main__':
    load_dotenv()
    db=connect_to_db()
    app.run(debug=True)