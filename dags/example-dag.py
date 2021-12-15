from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.version import version
from datetime import datetime, timedelta
import pandas
import pyodbc



def as_pandas_DataFrame(cursor):
    names = [metadata[0] for metadata in cursor.description]
    return pandas.DataFrame([dict(zip(names, row)) for row in cursor], columns=names)

def return_query(query):
    cfg = {'DSN': 'SampleDSN', 'host': 'quickstart.cloudera',
           'port': 21050,
           'username': 'cloudera', 'password': 'cloudera'}
    conn_string = f'Driver=Cloudera Impala ODBC Driver 64-bit; Host={cfg["host"]}; Port={cfg["port"]};' \
                  f' UID = {cfg["username"]}; PWD = {cfg["password"]}; ' \
                  'SSL = 1; '


    conn = pyodbc.connect(conn_string, autocommit=True)
    cursor = conn.cursor()
    cursor.execute(query)
    df = as_pandas_DataFrame(cursor)
    conn.close()
    print(df)
    return df




# Default settings applied to all tasks
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'catchup': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Using a DAG context manager, you don't have to specify the dag property of each task
with DAG('example_dag',
         start_date=datetime(2019, 1, 1),
         max_active_runs=3,
         schedule_interval=timedelta(minutes=30),  # https://airflow.apache.org/docs/stable/scheduler.html#dag-runs
         default_args=default_args,
         # catchup=False # enable if you don't want historical dag runs to run
         ) as dag:

    t0 = DummyOperator(
        task_id='start'
    )


    t1 = PythonOperator(
        task_id=f'execute_impala_query',
        python_callable=return_query,  # make sure you don't include the () of the function
        op_kwargs={'query': "SHOW DATABASES"},
    )





    t0 >> t1
