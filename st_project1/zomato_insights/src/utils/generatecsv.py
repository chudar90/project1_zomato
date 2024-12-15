from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

# Initialize Faker for generating fake data
fake = Faker()

# Function to generate synthetic customer data
def generate_customers(num=100):
    customers = []
    for customer_id in range(1, num + 1):
        customers.append({
            "customer_id": customer_id,  # Integer ID
            "name": fake.name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "location": fake.address(),
            "signup_date": fake.date_between(start_date='-2y', end_date='today'),
            "is_premium": fake.boolean(),
            "preferred_cuisine": random.choice(["Indian", "Chinese", "Italian", "Mexican"]),
            "total_orders": random.randint(1, 50),
            "average_rating": round(random.uniform(3.0, 5.0), 1)
        })
    return pd.DataFrame(customers)

# Function to generate synthetic restaurant data
def generate_restaurants(num=50):
    restaurants = []
    for restaurant_id in range(1, num + 1):
        restaurants.append({
            "restaurant_id": restaurant_id,  # Integer ID
            "name": fake.company(),
            "cuisine_type": random.choice(["Indian", "Chinese", "Italian", "Mexican"]),
            "location": fake.address(),
            "owner_name": fake.name(),
            "average_delivery_time": random.randint(15, 45),
            "contact_number": fake.phone_number(),
            "rating": round(random.uniform(3.0, 5.0), 1),
            "total_orders": random.randint(1, 500),
            "is_active": fake.boolean()
        })
    return pd.DataFrame(restaurants)

# Function to generate synthetic order data
def generate_orders(customers, restaurants, num=100):
    orders = []
    for order_id in range(1, num + 1):
        order_date = fake.date_this_year()
        delivery_time = order_date + timedelta(minutes=random.randint(30, 120))
        orders.append({
            "order_id": order_id,  # Integer ID
            "customer_id": random.choice(customers)['customer_id'],
            "restaurant_id": random.choice(restaurants)['restaurant_id'],
            "order_date": order_date,
            "delivery_time": delivery_time,
            "status": random.choice(["Pending", "Delivered", "Cancelled"]),
            "total_amount": random.randint(100, 1000),
            "payment_mode": random.choice(["Credit Card", "Cash", "UPI"]),
            "discount_applied": random.randint(0, 100),
            "feedback_rating": round(random.uniform(1.0, 5.0), 1)
        })
    return pd.DataFrame(orders)

# Function to generate synthetic delivery data
def generate_deliveries(orders, delivery_persons, num=100):
    deliveries = []
    for delivery_id in range(1, num + 1):
        delivery_time = random.randint(20, 60)
        estimated_time = random.randint(15, 50)
        deliveries.append({
            "delivery_id": delivery_id,  # Integer ID
            "order_id": random.choice(orders)['order_id'],  # Relates to orders
            "delivery_person_id": random.choice(delivery_persons)['delivery_person_id'],  # References delivery_persons ID
            "delivery_status": random.choice(["On the way", "Delivered"]),
            "distance": round(random.uniform(1, 15), 2),
            "delivery_time": delivery_time,
            "estimated_time": estimated_time,
            "delivery_fee": random.randint(20, 100),
            "vehicle_type": random.choice(["Bike", "Car", "Scooter"])
        })
    return pd.DataFrame(deliveries)

# Function to generate synthetic delivery person data
def generate_delivery_persons(num=20):
    delivery_persons = []
    for delivery_person_id in range(1, num + 1):
        delivery_persons.append({
            "delivery_person_id": delivery_person_id,  # Integer ID
            "name": fake.name(),
            "contact_number": fake.phone_number(),
            "vehicle_type": random.choice(["Bike", "Car", "Scooter"]),
            "total_deliveries": random.randint(1, 100),
            "average_rating": round(random.uniform(3.0, 5.0), 1),
            "location": fake.address()
        })
    return pd.DataFrame(delivery_persons)

# Generate data
customers_df = generate_customers(100)
restaurants_df = generate_restaurants(50)
orders_df = generate_orders(customers_df.to_dict(orient="records"), restaurants_df.to_dict(orient="records"), 100)
delivery_persons_df = generate_delivery_persons(20)  # Generate delivery persons first
deliveries_df = generate_deliveries(orders_df.to_dict(orient="records"), delivery_persons_df.to_dict(orient="records"), 100)

# Save data to CSV files
customers_df.to_csv('zomato_insights/data/customers.csv', index=False)
restaurants_df.to_csv('zomato_insights/data/restaurants.csv', index=False)
orders_df.to_csv('zomato_insights/data/orders.csv', index=False)
deliveries_df.to_csv('zomato_insights/data/deliveries.csv', index=False)
delivery_persons_df.to_csv('zomato_insights/data/delivery_persons.csv', index=False)

print("Synthetic data generated and saved successfully!")
