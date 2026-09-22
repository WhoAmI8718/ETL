
import csv
import logging

from config import DATA_FILE

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = {
    "id",
    "name",
    "category",
    "price",
    "quantity",
    "brand",
    "color",
    "available",
}


def extract_csv() -> tuple[list[dict[str, str]], int]:

    if not DATA_FILE.is_file():
        raise FileNotFoundError(
            f"CSV-файл не найден: {DATA_FILE}"
        )

    rows = []
    rejected_count = 0

    with DATA_FILE.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(
            file,
            delimiter=";"
        )

        # Проверяем структуру самого CSV-файла
        if reader.fieldnames is None:
            raise ValueError(
                "CSV-файл пустой или не содержит заголовка"
            )

        missing_columns = (
            REQUIRED_COLUMNS - set(reader.fieldnames)
        )

        if missing_columns:
            raise ValueError(
                f"В CSV отсутствуют столбцы: "
                f"{sorted(missing_columns)}"
            )

        # Обрабатываем строки файла
        for row in reader:

            if None in row or any(
                value is None for value in row.values()
            ):

                rejected_count += 1

                logger.warning(
                    "Строка CSV %s отклонена: "
                    "неверное количество полей. Данные: %s",
                    reader.line_num,
                    row
                )

                continue

            rows.append(row)

    return rows, rejected_count