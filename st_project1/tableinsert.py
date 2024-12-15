from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, Date, ForeignKey, Float, DECIMAL, Text
from sqlalchemy.exc import OperationalError

# Database connection setup
DATABASE_URL = "mysql+pymysql://root:@localhost/zomato_insights"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Function to dynamically create tables
def create_table(name, columns):
    try:
        Table(
            name,
            metadata,
            *columns,
            extend_existing=True  # Ensures tables are updated if already exist
        )
        metadata.create_all(engine)
        print(f"Table '{name}' created successfully.")
    except OperationalError as e:
        print(f"Error creating table '{name}': {e}")

# Define columns dynamically for all tables

# Customers Table Columns
customers_columns = [
    Column("customer_id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False),
    Column("email", String(255), nullable=False, unique=True),
    Column("phone", String(15), nullable=False),
    Column("location", Text),
    Column("signup_date", Date, nullable=False),
    Column("is_premium", Boolean, default=False),
    Column("preferred_cuisine", String(100)),
    Column("total_orders", Integer, default=0),
    Column("average_rating", DECIMAL(3, 2))
]

# Restaurants Table Columns
restaurants_columns = [
    Column("restaurant_id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False),
    Column("cuisine_type", String(100)),
    Column("location", Text),
    Column("owner_name", String(255)),
    Column("average_delivery_time", Integer, default=30),
    Column("contact_number", String(15)),
    Column("rating", DECIMAL(3, 2)),
    Column("total_orders", Integer, default=0),
    Column("is_active", Boolean, default=True)
]

# Delivery Persons Table Columns
delivery_persons_columns = [
    Column("delivery_person_id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
    Column("contact_number", String(15)),
    Column("vehicle_type", String(50)),
    Column("total_deliveries", Integer, default=0),
    Column("average_rating", DECIMAL(3, 2)),
    Column("location", Text)
]

# Orders Table Columns
orders_columns = [
    Column("order_id", Integer, primary_key=True, autoincrement=True),
    Column("customer_id", Integer, ForeignKey('Customers.customer_id'), nullable=False),
    Column("restaurant_id", Integer, ForeignKey('Restaurants.restaurant_id'), nullable=False),
    Column("order_date", Date, nullable=False),
    Column("delivery_time", Date),
    Column("status", String(50)),
    Column("total_amount", Float),
    Column("payment_mode", String(50)),
    Column("discount_applied", Float, default=0),
    Column("feedback_rating", DECIMAL(3, 2))
]

# Deliveries Table Columns
deliveries_columns = [
    Column("delivery_id", Integer, primary_key=True, autoincrement=True),
    Column("order_id", Integer, ForeignKey('Orders.order_id'), nullable=False),
    Column("delivery_person_id", Integer, ForeignKey('DeliveryPersons.delivery_person_id')),
    Column("delivery_status", String(50)),
    Column("distance", Float),
    Column("delivery_time", Integer),
    Column("estimated_time", Integer),
    Column("delivery_fee", Float),
    Column("vehicle_type", String(50))
]

# Dynamically create all tables in dependency order
create_table("Customers", customers_columns)
create_table("Restaurants", restaurants_columns)
create_table("DeliveryPersons", delivery_persons_columns)  # DeliveryPersons must be created before Deliveries
create_table("Orders", orders_columns)  # Orders must be created before Deliveries
create_table("Deliveries", deliveries_columns)  # Deliveries is dependent on Orders and DeliveryPersons
