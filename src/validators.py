
def quantity_check(value: int) -> int:
    if value < 0:
        raise ValueError("Количество товара не может быть отрицательным")

    return value

def row_check(value: str) -> str:
    value = value.strip()

    if not value:
        raise ValueError(
        "Название и категория не могут быть пустыми"
    )

    return value