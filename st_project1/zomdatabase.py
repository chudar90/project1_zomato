import pymysql

class Database:
    def __init__(self, host, user, password, database):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='zomato_insights'
        )
        self.cursor = self.connection.cursor()
        
    def execute_query(self, query, params=None):
        """Executes a SQL query and commits the transaction."""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            print(f"Error executing query: {e}")

    def fetch_query(self, query):
        """Fetches results from a SELECT query."""
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def fetch_peak_order_times(self):
        query = """
        SELECT HOUR(order_date) AS order_hour, COUNT(*) AS order_count
        FROM orders
        GROUP BY order_hour
        ORDER BY order_count DESC;
        """
        return self.fetch_query(query)

    def fetch_top_locations_for_orders(self):
        query = """
        SELECT location, COUNT(*) AS order_count
        FROM orders
        JOIN customers ON orders.customer_id = customers.customer_id
        GROUP BY location
        ORDER BY order_count DESC;
        """
        return self.fetch_query(query)

    def fetch_delayed_deliveries(self):
        query = """
        SELECT order_id, order_date, delivery_time, TIMESTAMPDIFF(MINUTE, order_date, delivery_time) AS delay_duration
        FROM orders
        WHERE TIMESTAMPDIFF(MINUTE, order_date, delivery_time) > 30;
        """
        return self.fetch_query(query)

    def fetch_top_customers(self):
        query = """
        SELECT customer_id, COUNT(*) AS order_count
        FROM orders
        GROUP BY customer_id
        ORDER BY order_count DESC
        LIMIT 10;
        """
        return self.fetch_query(query)

    def fetch_customer_preferences(self):
        query = """
        SELECT preferred_cuisine, COUNT(*) AS order_count
        FROM orders
        JOIN customers ON orders.customer_id = customers.customer_id
        GROUP BY preferred_cuisine
        ORDER BY order_count DESC;
        """
        return self.fetch_query(query)

    def fetch_orders_by_location(self):
        query = """
        SELECT location, COUNT(*) AS order_count
        FROM orders
        JOIN customers ON orders.customer_id = customers.customer_id
        GROUP BY location;
        """
        return self.fetch_query(query)
    
    def fetch_orders_by_value(self):
        query = """
        SELECT order_id, order_value
        FROM orders
        ORDER BY order_value DESC
        LIMIT 10;
        """
        return self.fetch_query(query)

    def add_customer(self, name,  email , phone, location, signup_date, preferred_cuisine, total_orders, average_rating ):
        query = "INSERT INTO customers (name, email, phone, location, signup_date, preferred_cuisine,total_orders, average_rating) VALUES (%s, %s,%s, %s, %s, %s, %s, %s )"
        self.execute_query(query, (name, email , phone, location, signup_date, preferred_cuisine, total_orders, average_rating ))

    def fetch_customers(self):
        query = "SELECT * FROM customers"
        return self.fetch_query(query)
    
    def fetch_orders(self):
        query = "SELECT * FROM orders"
        return self.fetch_query(query)
    
    def fetch_restaurants(self):
        query = "SELECT * FROM restaurants"
        return self.fetch_query(query)
    
    def create_table(self, table_name, columns):
        query = f"CREATE TABLE {table_name} ({', '.join([f'{col} {dtype}' for col, dtype in columns.items()])});"
        self.execute_query(query)  

    def add_column(self, table_name, column_name, column_type):
        query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};"
        self.execute_query(query) 

    def search_customers(self, name):
        query = "SELECT * FROM customers WHERE name LIKE %s"
        self.cursor.execute(query, (f"%{name}%",))
        return self.cursor.fetchall()