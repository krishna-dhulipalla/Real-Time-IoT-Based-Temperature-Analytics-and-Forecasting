from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id='data_refresh',
    start_date=datetime(2024, 1, 1),
    schedule='@hourly',
    catchup=False,
) as dag:

    generate_data = BashOperator(
        task_id='generate_data',
        bash_command='python sensor_pipeline.py'
    )
