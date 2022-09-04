import pandas as pd


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


