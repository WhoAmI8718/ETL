from datetime import datetime
from decimal import Decimal
import json
import logging
from pathlib import Path
import re
import sys

from airflow.sdk import dag, get_current_context, task


sys.path.insert(0, "/opt/airflow/project/src")

from extract import extract_csv
from load import load
from transform import transform


logger = logging.getLogger(__name__)

STAGING_DIR = Path("/opt/airflow/project/data/staging")


def create_staging_path(stage: str) -> Path:
    context = get_current_context()
    run_id = context["run_id"]

    safe_run_id = re.sub(
        r"[^a-zA-Z0-9_.-]",
        "_",
        run_id,
    )

    STAGING_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    return STAGING_DIR / f"{safe_run_id}_{stage}.json"


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
        rows, rejected_count = extract_csv()

        output_path = create_staging_path("extracted")

        output_path.write_text(
            json.dumps(
                rows,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return {
            "path": str(output_path),
            "row_count": len(rows),
            "rejected_count": rejected_count,
        }

    @task
    def transform_task(extract_result):
        input_path = Path(extract_result["path"])

        rows = json.loads(
            input_path.read_text(encoding="utf-8")
        )

        products, transform_rejected = transform(rows)

        output_path = create_staging_path("transformed")

        output_path.write_text(
            json.dumps(
                products,
                ensure_ascii=False,
                default=str,
            ),
            encoding="utf-8",
        )

        return {
            "path": str(output_path),
            "product_count": len(products),
            "rejected_count": (
                extract_result["rejected_count"]
                + transform_rejected
            ),
        }

    @task
    def load_task(transform_result):
        input_path = Path(transform_result["path"])

        products = json.loads(
            input_path.read_text(encoding="utf-8")
        )

        # JSON не имеет типа Decimal, поэтому восстанавливаем его.
        for product in products:
            product["price"] = Decimal(product["price"])

        load(products)

        return {
            "loaded_count": len(products),
            "rejected_count": transform_result["rejected_count"],
        }

    @task
    def report_task(load_result):
        logger.info(
            "Загружено: %s, отклонено: %s",
            load_result["loaded_count"],
            load_result["rejected_count"],
        )

    extracted = extract_task()
    transformed = transform_task(extracted)
    loaded = load_task(transformed)
    report_task(loaded)


products_etl()