from decimal import Decimal
from unittest.mock import MagicMock, patch

from load import load

import psycopg
import pytest


def test_load_executes_upsert():
    products = [
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

    fake_connection_string = "postgresql://test"

    connection_manager = MagicMock()
    connection = connection_manager.__enter__.return_value

    cursor_manager = connection.cursor.return_value
    cursor = cursor_manager.__enter__.return_value

    with patch(
        "load.psycopg.connect",
        return_value=connection_manager,
    ) as connect_mock:
        load(
            products,
            fake_connection_string,
        )

    connect_mock.assert_called_once_with(
        fake_connection_string
    )

    cursor.executemany.assert_called_once()

    query, rows = cursor.executemany.call_args.args

    assert "ON CONFLICT (csvid)" in query

    assert rows == [
        (
            1,
            "Mouse",
            "Electronics",
            Decimal("99.90"),
            2,
            "Logitech",
            "Black",
            True,
        )
    ]

def test_load_reraises_database_error():
    database_error = psycopg.OperationalError(
        "Database is unavailable"
    )

    with patch(
        "load.psycopg.connect",
        side_effect=database_error,
    ):
        with pytest.raises(
            psycopg.OperationalError,
            match="Database is unavailable",
        ):
            load(
                [],
                "postgresql://test",
            )