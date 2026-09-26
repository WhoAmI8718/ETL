from datetime import datetime
import sys

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator


sys.path.insert(0, "/opt/airflow/project/src")

from main import main


with DAG(
    dag_id="products_etl",
    start_date=datetime(2026, 9, 1),
    schedule=None,
    catchup=False,
    tags=["etl", "products"],
) as dag:

    run_etl = PythonOperator(
        task_id="run_etl",
        python_callable=main,
    )