import pandas as pd
import requests
import os

def get_repo_list_from_csv():
    try:
        df = pd.read_csv('repo.csv')
        repos=[]
        for index,row in df.iterrows():
            repos.append([row['repo_name'],row['owner']])
        return repos
    except Exception as e:
        print(e)
        print("Unable to read csv file")


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


