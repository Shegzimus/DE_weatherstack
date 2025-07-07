from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
dag = DAG(
    dag_id="orchestrator",
    default_args=default_args,
    schedule=None,
    catchup=False
)

with dag:
    task1 = PythonOperator(
        task_id="task1",
        python_callable=lambda: print("Task 1 executed"),
        dag=dag
    )