from zomdatabase import Database

# Initialize the database connection
db = Database(host="localhost", user="root", password="", database="zomato_insights")

# Test: Add a customer
db.add_customer("John Doe", "New York")

# Test: Fetch customers
customers = db.fetch_customers()
print(customers)

# You can also add more tests to test other methods
# For example, testing adding an order:
# db.add_order(customer_id=1, restaurant_id=1, order_date="2024-12-01", order_value=30.5)
