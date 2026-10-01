from typing import Any

import psycopg
import logging

logger = logging.getLogger(__name__)


def load(
    products: list[dict[str, Any]],
    db_connection: str,
) -> None:
    rows = [
        (
            product["csvid"],
            product["name"],
            product["category"],
            product["price"],
            product["quantity"],
            product["brand"],
            product["color"],
            product["available"],
        )
        for product in products
    ]

    query = """
        INSERT INTO fullproducts(
            csvid,
            name,
            category,
            price,
            quantity,
            brand,
            color,
            available
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)

        ON CONFLICT (csvid)
        DO UPDATE SET
        name = EXCLUDED.name,
        category = EXCLUDED.category,
        price = EXCLUDED.price,
        quantity = EXCLUDED.quantity,
        brand = EXCLUDED.brand,
        color = EXCLUDED.color,
        available = EXCLUDED.available;
    """

    try:
      with psycopg.connect(db_connection) as conn:
        with conn.cursor() as cur:
            cur.executemany(query, rows)

      logger.info(
       "Загрузка завершена. Обработано строк: %s",
        len(rows)
      )
    except psycopg.Error:
      logger.exception(
          "Ошибка при загрузке товаров. "
          "Транзакция откатана."
      )

      raise