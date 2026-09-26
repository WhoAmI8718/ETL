from datetime import datetime
import sys

from airflow.sdk import dag, task

sys.path.insert(0, "/opt/airflow/project/src")

from extract import extract_csv
from transform import transform
from load import load


CSV_PATH = "/opt/airflow/project/data/products_10x10.csv"


@dag(
    dag_id="products_etl",
    start_date=datetime(2026, 9, 1),
    schedule=None,
    catchup=False,
    tags=["etl", "products"],
)
def products_etl():

    @task
    def extract_task():
        rows, rejected_count = extract_csv(CSV_PATH)

        return {
            "rows": rows,
            "rejected_count": rejected_count,
        }

    @task
    def transform_task(extract_result):
        rows = extract_result["rows"]

        products, rejected_count = transform(rows)

        return {
            "products": products,
            "rejected_count": rejected_count,
        }

    @task
    def load_task(transform_result):
        products = transform_result["products"]

        load(products)

    extracted = extract_task()

    transformed = transform_task(extracted)

    load_task(transformed)


products_etl()