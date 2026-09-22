import csv
import psycopg

products = []
DB_CONNECTION= "postgresql://postgres:@localhost:5432/postgres"

with open("D:\\NewPython\\data\\products_10x10.csv", "r", encoding="utf-8-sig") as file:
  reader = csv.DictReader(file, delimiter=";")

  for row in reader:
    product = {
      "name" : row["name"].strip(),
      "category" : row["category"].strip(),
      "price" : float(row["price"].replace(",", ".")),
      "quantity" : int(row["quantity"]),
      "brand" : row["brand"].strip(), 
      "color" : row["color"].strip(),
      "available" : row["available"].strip().lower() == "true"
    }

    products.append(product)

  print(*products, sep="\n")

rows = []

for product in products:
    rows.append(
        (
            product["name"],
            product["category"],
            product["price"],
            product["quantity"],
            product["brand"],
            product["color"],
            product["available"]
        )
    )

with psycopg.connect(DB_CONNECTION) as conn:
  with conn.cursor() as cur:
    cur.executemany(
      """insert into fullproducts(name, category, price, quantity, brand, color, available)
      values(%s, %s, %s, %s, %s, %s, %s)""",
      rows
    )
