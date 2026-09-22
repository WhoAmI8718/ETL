"""
print("Привет Настя!")

name = "Настя"
age = 22
sex = True 
agepoint = 22.5
noting = None
cache = "100"

print(type(name))
print(type(age))
print(type(sex))
print(type(agepoint))
print(type(noting))

print("--------------------------------")

print("У Насти есть " + cache + "$")

cache = int(cache) + 50
print(type(cache))

print("У Насти есть " + str(cache) + "$")

print("--------------------------------")


valueCache = int(input("Введите число: ")) ##

##print("--------------------------------")
##print(type(valueCache))
##print("--------------------------------")
##valueCache = int(valueCache)
##print("--------------------------------")
##print(type(valueCache))
##print("--------------------------------")

if valueCache > 0:
    print("Ваш баланс " + str(valueCache) + "$")
elif valueCache == 0:
    print("Ваш баланс пуст")
    if name == "Настя":
        print("У " + str(name) + " есть " + str(valueCache) + "$")  
else:
    print("Ваш баланс отрицательный")


print("--------------------------------")

prices = [100, 200, 300, 400, 500]
newprice = []

for p in prices:
    if p > 200:
      newprice.append(p)

print(newprice)

print("--------------------------------")
count = 0 

while count < len(prices):
  if prices[count] >= 200:
     print(prices[count])
  count += 1 
print("--------------------------------")

# Список
list_name = ["Alex", "Melmon", "Glory", "Marty"]

list_name.append("Shceper")

list_name.insert(5, "Kovalski")

list_name.append("Redovoy")
list_name.append("Redovoy")

print(list_name)

count = list_name.index("Redovoy")
list_name[count] = "Rico"

print(list_name)
print("--------------------------------")

list_name.append("Redovoy")

print(list_name)
print("--------------------------------")

list_name.remove("Redovoy")

print(list_name)
print("--------------------------------")

# Работа со Словарем
products = [
    {"id": 1, "name": "Phone", "price": 1000},
    {"id": 2, "name": "Camera", "price": 800},
    {"id": 3, "name": "TV", "price": 2500},
    {"id": 4, "name": "TVs", "price": 3500},
    {"id": 5, "name": "Lolypop", "price": 1}
]

for product in products:
    print(product["name"], product["price"])

print("--------------------------------")

#for i in products:
#    print(i["name"], i["price"])

for product in products:
    if product["name"] == "TVs":
        product["name"] = "Micro"

    print(product)
print("--------------------------------")

for prod in products:
    prod["garanty"] = True

print(prod)
print("--------------------------------")

for p in products:
    print(p)

print("--------------------------------")

products[2]["garanty"] = False 

del products[4]["garanty"]

for p in products:
    print(p)
print("--------------------------------")

for pip in products:
    if pip["id"] == 5:
        products.remove(pip)


for p in products:
    print(p)
print("--------------------------------")


name1 = "Привет мир я в рот "
name2 = "Привет мир я в рот "
name3 = "Привет мир я в рот "
name4 = "Привет мир я в рот "

print(name1.strip()) #Удалят пробелы в начале и конце
print(name2.lower())
print(name3.upper())
print(name4.replace("рот", "рот ебал"))
print("--------------------------------")

# F-Строки
name_calculate5 = 6
name_calculate6 = 7

print(f"Вычисляем: {name_calculate5 + name_calculate6}")

name = "OZON"
print(f"{name.lower()}")
print("--------------------------------")

#page.click_element(f'Нажатие на вкладку {tab_title}', page.selectors['menu_tab'].format(tab_state))


#Функции
products = [
    {"id": 1, "name": "Phone", "price": 1000},
    {"id": 2, "name": "Camera", "price": 800},
    {"id": 3, "name": "TV", "price": 2500},
    {"id": 4, "name": "TVs", "price": 3500},
    {"id": 5, "name": "Lolypop", "price": 1}
]

min_price = int(input("Введите минимальное: " ))

def short_price_fillter(products, min_price):
    count = 0

    while count < len(products):
      if products[count]["price"] < min_price:
          print(products[count]["name"])
      else:
          print("Вот такая вот Хуйня")

      count += 1

def short_price_fillter2(products, min_price):
    for prod in products:
        if prod["price"] < min_price:
            print (prod["name"])
        else:
            print("Вот такая вот Хуйня Dog") 

#short_price_fillter(products, min_price)

#short_price_fillter2(products, min_price)

def short_price_fillter_return(products, min_price):
    result = []

    for prod in products:
        if prod["price"] < min_price:
            result.append(prod)

    return result 

res = short_price_fillter_return(products, min_price)
print(*res, sep="\n") ### Перенос на новую строку ::Fier

name = input("Введите наименование: ")            
def normalize_name(name):
    return name.strip().lower()

print (f"Наверное вы хотели {normalize_name(name)}")


#Try / except
try:
    age = int(input("Введите возраст: "))
    print(age)

except ValueError:
    print("Нужно ввести число")

finally:
    age = 1 
    print(age)

#ValueError	значение неправильного формата
#ZeroDivisionError	деление на 0
#KeyError	нет ключа в dict
#IndexError	нет такого индекса в списке
#TypeError	неправильный тип данных
#FileNotFoundError	файл не найден

#try       → попробуй
#except    → если ошибка
#else      → если ошибки нет
#finally   → выполнить всегда

### Работа с Файлами

import csv

products = []

with open(r"D:\\NewPython\\data\\products_10x10.csv", "r", encoding="utf-8-sig") as file: #utf-8
    reader = csv.DictReader(file, delimiter=";")
    #print(reader.fieldnames)
    for row in reader:
        row["name"] = row["name"].strip()
        row["category"] = row["category"].strip()
        row["brand"] = row["brand"].strip() 
        row["color"] = row["color"].strip() 
        row["weight"] = float(row["weight"].replace(",", "."))
        row["available"] = bool(row["available"].strip())
        row["rating"] = float(row["rating"].replace(",", "."))
        products.append(row)
print(sep="\n")
print(*products, sep="\n")
print(sep="\n")

# JSON превращаешь его в обычный Python-словарь
print("--------------------------------")
import json

text = '''
{
  "id": 1,
  "name": "Iphone",
  "price": 1200
}
'''

data = json.loads(text)

prod = json.dumps(data, indent=4) ##Fier

print(data)
print(prod)
#JSON-текст
#    ↓
#json.loads()
#    ↓
#Python dict
print("--------------------------------")

# Каждую строку CSV превращай в словарь
print("--------------------------------")
import csv 

with open(r"D:\\NewPython\\data\\Some.csv", "r", encoding="utf-8-sig")as file: 
  reader = csv.DictReader(file, delimiter=";")
  #print(reader.fieldnames)
  for row in reader:
    try:
      print(row["product"], row["price"])
    except KeyError:
      print("Скорректируйте колонку в файле, проверте синтаксис")

print("--------------------------------")

#requests: получение данных из API
import requests
import json

url = "https://jsonplaceholder.typicode.com/posts"
response = requests.get(url, timeout=30)
response.raise_for_status()

data = response.json()
prod = json.dumps(data[0], indent=4)
print(prod)

print("--------------------------------")
#GET-запросы к API timeout=30 ждать ответа максимум 30 секунд
headers = {
    "Authorization": "Bearer YOUR_TOKEN"
}

response = requests.get(url, headers=headers, timeout=30)
print("--------------------------------")

params = {
    "limit": 5,
    "page": 1
}

response = requests.get(url, params=params, timeout=30)

print("--------------------------------")
import requests
import json

url = "https://jsonplaceholder.typicode.com/posts"

params = {
    "_limit": 5
}

response = requests.get(
    url,
    params=params,
    timeout=30
)

print("Итоговый URL:")
print(response.url)

print("\nСтатус:")
print(response.status_code)

print("\nОтвет сервера:")
print(response.json())

products = response.json()

prod = json.dumps(products, indent=4)

print("\nКрасивый JSON:")
print(prod)

for post in products:
    print(post["id"], post["title"])

print("--------------------------------")

for page in range(1, 4):

    params = {
        "_limit": 5,
        "_page": page
    }

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    posts = response.json()

    print(f"\nСтраница {page}")

    for post in posts:
        print(post["id"], post["title"])

#Даты и время
from datetime import datetime

text = "2026-09-16T12:30:00"
dt = datetime.fromisoformat(text)
print(dt.date())
print(dt.year)
from datetime import datetime, timezone

loaded_at = datetime.now(timezone.utc)
print(loaded_at)


raw_products = [
    {"id": "1", "name": "  Phone ", "price": "1250.50"},
    {"id": "2", "name": "Camera", "price": "900"}
]

clean_products = []

for row in raw_products:
    clean_products.append({
        "id": int(row["id"]),
        "name": row["name"].strip(),
        "price": float(row["price"])
    })

print(clean_products)

print("--------------------------------")

#PostgreSQL из Python
import psycopg 

conn = psycopg.connect(
  "host=localhost dbname=postgres user=postgres"
)

with conn.cursor() as cur:
  cur.execute("select * from users")
  print(cur.fetchone()) # Jlyf pfgbcm

conn.close()
print("--------------------------------")

import psycopg 

conn = psycopg.connect(
  "host=localhost dbname=postgres user=postgres"
)

with conn.cursor() as cur:
  cur.execute("select * from users limit 10")
  print(cur.fetchall()) # все записи 

conn.close()
print("--------------------------------")

#INSERT
import psycopg 

conn = psycopg.connect(
  "host=localhost dbname=postgres user=postgres"
)

with conn.cursor() as cur:
  cur.execute(
            """ 
"""
            INSERT INTO products(name, price)
            VALUES (%s, %s)
            """
""",
            ("Phone", 1250.50)
        )
conn.commit()

conn.close()
print("--------------------------------")

# Несколько записей 
import psycopg 

rows = [
    ("IPhone", 1550.50),
    ("Camera", 900.00)
]
#with psycopg.connect(DATABASE_URL) as conn:
conn = psycopg.connect(
  "host=localhost dbname=postgres user=postgres"
)

with conn.cursor() as cur:
    cur.executemany(
        "INSERT INTO products(name, price) VALUES (%s, %s)",
        rows
    )
conn.commit()

conn.close()

# case конструкция 
a = float(input())
b = float(input())
operation = input()

if operation in ('/', 'mod', 'div') and b == 0:
    print("Деление на 0!")
else:
    match operation:
        case "+":
            print(a + b)
        case "-":
            print(a - b)
        case "*":
            print(a * b)
        case "/":
            print(a / b)
        case "mod":
            print(a % b)
        case "pow":
            print(a ** b)
        case "div":
            print(a // b)
"""
s = 'abcdefghijk'
print(s[3:6])
print(s[:6])
print(s[3:])
print(s[::-1])
print(s[-3:])
print(s[:-6])
print(s[-1:-10:-2])