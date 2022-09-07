# github-activity-analyzer

## Getting Started
1. Clone the repo - 
```
git clone https://github.com/Pratyush-Saxena/github-activity-analyzer
```

2. Install the requirements -
```
pip3 install -r requirements.txt
```

3. Export airflow path
```
export AIRFLOW_HOME=airflow FLASK_APP=main.py
```

4. Make script executable -
```
chmod +x airflow.sh
```

5. Now run airflow script
```
./airflow.sh bash
```

6. Now open airflow web at http://0.0.0.0:8181 (username - admin) and run the dag manually.
![Screenshot from 2022-09-07 14-15-32](https://user-images.githubusercontent.com/52444607/188833707-df257ca7-e481-41fa-883b-36969ca7e5a4.png)

7. Run flask server ( NOTE: Setup the local postgres database and update the values in .env file before running server)
```
flask run 
```
8. Go to http://127.0.0.1:5000/github/repo/stats/apache/airflow and you will see todays stats of the repo apache/airflow
