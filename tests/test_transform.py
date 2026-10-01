from decimal import Decimal

from transform import transform

import pytest


def test_transform_valid_row():
    # Arrange — подготавливаем входные данные
    rows = [
        {
            "id": "1",
            "name": " Mouse ",
            "category": " Electronics ",
            "price": "99,90",
            "quantity": "2",
            "brand": " Logitech ",
            "color": " Black ",
            "available": "true",
        }
    ]

    # Act — вызываем проверяемую функцию
    products, rejected_count = transform(rows)

    # Assert — проверяем результат
    assert rejected_count == 0

    assert products == [
        {
            "csvid": 1,
            "name": "Mouse",
            "category": "Electronics",
            "price": Decimal("99.90"),
            "quantity": 2,
            "brand": "Logitech",
            "color": "Black",
            "available": True,
        }
    ]

def test_transform_rejects_negative_quantity():
    rows = [
        {
            "id": "1",
            "name": "Mouse",
            "category": "Electronics",
            "price": "99.90",
            "quantity": "-1",
            "brand": "Logitech",
            "color": "Black",
            "available": "true",
        }
    ]

    products, rejected_count = transform(rows)

    assert products == []
    assert rejected_count == 1

def make_valid_row() -> dict[str, str]:
    return {
        "id": "1",
        "name": "Mouse",
        "category": "Electronics",
        "price": "99.90",
        "quantity": "2",
        "brand": "Logitech",
        "color": "Black",
        "available": "true",
    }

rows = [make_valid_row()]

@pytest.mark.parametrize(
    ("field", "invalid_value"),
    [
        ("price", "not-a-number"),
        ("quantity", "-1"),
        ("available", "yes"),
        ("name", "   "),
    ],
)
def test_transform_rejects_invalid_value(
    field: str,
    invalid_value: str,
):
    row = make_valid_row()
    row[field] = invalid_value

    products, rejected_count = transform([row])

    assert products == []
    assert rejected_count == 1