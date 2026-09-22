from decimal import Decimal, InvalidOperation

def parse_price(value: str) -> Decimal:
    try:
        price = Decimal(
            value.strip().replace(",", ".")
        )
    except InvalidOperation as exc:
        raise ValueError(
            f"Некорректная цена: {value!r}"
        ) from exc

    if not price.is_finite():
        raise ValueError("Цена должна быть конечным числом")

    if price < 0:
        raise ValueError("Цена не может быть отрицательной")

    return price

def parse_bool(value: str) -> bool:
    normalized = value.strip().lower()

    if normalized == "true":
        return True

    if normalized == "false":
        return False

    raise ValueError(
        f"Недопустимое значение available: {value!r}"
    )