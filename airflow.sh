

# check for the existence of airflow.db file in tmp
if [ ! -f /tmp/airflow.db ]; then
    # if it doesn't exist, create it
    airflow db init && airflow users create     --username admin     --firstname airflow     --lastname admin     --role Admin     --email admin@airflow.web
fi

# run the airflow scheduler in the background
airflow scheduler & 

# run the airflow webserver
airflow webserver --port 8181

