from datetime import timedelta
import pendulum

from airflow.sdk import (
    Connection,
    CronDataIntervalTimetable,
    dag,
    get_current_context,
    task,
)

from decimal import Decimal
import json
import logging
from pathlib import Path
import re
import sys


sys.path.insert(0, "/opt/airflow/project/src")

from extract import extract_csv
from load import load
from transform import transform


logger = logging.getLogger(__name__)

STAGING_DIR = Path("/opt/airflow/project/data/staging")
MIN_PRODUCTS = 1


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
    start_date=pendulum.datetime(
        2026,
        9,
        1,
        tz="Europe/Moscow",
    ),
    schedule=CronDataIntervalTimetable(
    "*/5 * * * *",
    timezone="Europe/Moscow",
    ),
    catchup=False,
    tags=["etl", "products"],
)
def products_etl():

    @task
    def interval_info_task():
      context = get_current_context()
      
      logger.info(
          "run_id: %s",
          context["run_id"],
      )
      logger.info(
          "logical_date: %s",
          context["logical_date"],
      )
      logger.info(
          "data_interval_start: %s",
          context["data_interval_start"],
      )
      logger.info(
          "data_interval_end: %s",
          context["data_interval_end"],
      )

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

    @task(
      #retries=2,
      #retry_delay=timedelta(seconds=5),
    )
    def validate_task(transform_result):
        product_count = transform_result["product_count"]
    
        logger.info(
            "Проверка количества товаров: %s",
            product_count,
        )
    
        if product_count < MIN_PRODUCTS:
            raise ValueError(
                f"Слишком мало товаров: {product_count}. "
                f"Минимум: {MIN_PRODUCTS}"
            )
    
        return transform_result

    @task(
      #retries = 2,
      #retry_delay = timedelta(seconds = 5),
      #retry_exponential_backoff=True, # увеличивает задержку между повторными попытками.    
    )
    def load_task(transform_result):
        input_path = Path(transform_result["path"])

        products = json.loads(
            input_path.read_text(encoding="utf-8")
        )

        # JSON не имеет типа Decimal, поэтому восстанавливаем его.
        for product in products:
            product["price"] = Decimal(product["price"])

        connection = Connection.get("products_db")
        
        load(products,
             connection.get_uri(),
            )

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

    interval_info = interval_info_task()
    extracted = extract_task()
    
    interval_info >> extracted
    
    transformed = transform_task(extracted)
    validated = validate_task(transformed)
    loaded = load_task(validated)
    report_task(loaded)


products_etl()