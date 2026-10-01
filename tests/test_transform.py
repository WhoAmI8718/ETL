from decimal import Decimal

import pytest

from transform import transform


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


def test_transform_valid_row():
    rows = [make_valid_row()]

    products, rejected_count = transform(rows)

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