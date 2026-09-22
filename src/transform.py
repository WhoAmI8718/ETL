from typing import Any
import logging
from parsers import *
from validators import *

logger = logging.getLogger(__name__)


def transform(rows: list[dict[str, str]]) -> tuple[list[dict[str, Any]], int]:
    products = []
    rejected_count = 0
    set_id = set()

    for row in rows:
        try:
            product = {
                "csvid": int(row["id"]),
                "name": row_check(row["name"].strip()),
                "category": row_check(row["category"].strip()),
                "price": parse_price(row["price"]),
                "quantity": quantity_check(int(row["quantity"])),
                "brand": row["brand"].strip(),
                "color": row["color"].strip(),
                "available": parse_bool(row["available"]),
            }
            product_id = product["csvid"]

            if product_id in set_id:
                raise ValueError(
                      f"Повторяющийся csvid: {product_id}"
            )

            set_id.add(product_id)
            
            products.append(product)

        except (KeyError, ValueError) as exc:
            rejected_count += 1

            logger.warning(
                "Некорректная строка: %s. Ошибка: %s",
                row,
                exc
            )

    return products, rejected_count
