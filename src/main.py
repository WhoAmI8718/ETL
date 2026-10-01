
import logging

from extract import extract_csv
from transform import transform
from load import load

from config import get_local_db_connection


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(
            "etl.log",
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main() -> None:

    logger.info("Запуск ETL")

    # 1. EXTRACT
    rows, extract_rejected = extract_csv()

    # 2. TRANSFORM
    products, transform_rejected = transform(rows)

    # 3. СТАТИСТИКА
    read_count = len(rows) + extract_rejected

    valid_count = len(products)

    rejected_count = (
        extract_rejected + transform_rejected
    )

    load_count = len(products)

    logger.info("===== СТАТИСТИКА ETL =====")
    logger.info("Прочитано: %s", read_count)
    logger.info("Корректных: %s", valid_count)
    logger.info("Отклонено: %s", rejected_count)
    logger.info(
        "Передано на загрузку: %s",
        load_count
    )

    # 4. LOAD
    if not products:
        raise ValueError(
            "Нет корректных данных для загрузки"
        )

    load(products,
         get_local_db_connection(),
        )

    logger.info("ETL успешно завершён")


if __name__ == "__main__":
    main()