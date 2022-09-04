from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from utils import collect_repo_data

# def print_hello():
#     # collect_repo_data()
#     return "function called"

def data_collection():
    collect_repo_data()
    return "data collected"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": '2020-10-01',
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "github_data_collection",
    description="Simple tutorial DAG",
    schedule_interval="0 12 * * *",
    default_args=default_args,
    catchup=False,
)

t1 = PythonOperator(
    task_id="collect_data",
    python_callable=data_collection,
    dag=dag,
)


t0 = DummyOperator(task_id="dummy_task", retries=3, dag=dag)

# t2 = PythonOperator(task_id="hello_task", python_callable=print_hello, dag=dag)

# sets downstream foe t1
t0 >> t1