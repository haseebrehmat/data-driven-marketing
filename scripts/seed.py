import random
from connections import get_postgres_conn
import faker

fake = faker.Faker()

cursor = get_postgres_conn().cursor()

# Insert 1,000 dummy customers
customers = [(fake.name(), fake.email(), fake.address()) for _ in range(500)]
cursor.executemany(
    "INSERT INTO Customers (name, email, address) VALUES (%s, %s, %s)", customers
)

# Insert 100 dummy products
products = [
    (fake.word().capitalize(), fake.sentence(), round(random.uniform(10, 2000), 2))
    for _ in range(100)
]
cursor.executemany(
    "INSERT INTO Products (name, description, price) VALUES (%s, %s, %s)", products
)

# Fetch customer and product IDs
cursor.execute("SELECT customer_id FROM Customers")
customer_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT product_id FROM Products")
product_ids = [row[0] for row in cursor.fetchall()]

# Insert 10,000 dummy orders
orders = []
for _ in range(10000):
    orders.append(
        (
            random.choice(customer_ids),
            random.choice(product_ids),
            random.randint(1, 5),  # Quantity
            fake.date_time_this_decade(),  # Random order date
        )
    )

cursor.executemany(
    "INSERT INTO Orders (customer_id, product_id, quantity, order_date) VALUES (%s, %s, %s, %s)",
    orders,
)

# Fetch order IDs
cursor.execute("SELECT order_id FROM Orders")
order_ids = [row[0] for row in cursor.fetchall()]

# Insert 10,000 dummy sales
sales = []
for order_id in order_ids:
    sales.append(
        (
            order_id,
            round(random.uniform(50, 5000), 2),  # Random total amount
            fake.date_time_this_decade(),  # Random sale date
        )
    )

cursor.executemany(
    "INSERT INTO Sales (order_id, total_amount, sale_date) VALUES (%s, %s, %s)", sales
)

