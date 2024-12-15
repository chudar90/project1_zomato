import streamlit as st
import pandas as pd
from datetime import datetime
from zomdatabase import Database

# Initialize database connection
db = Database(host="localhost", user="root", password="", database="zomato_insights")

# Streamlit Customization for Red Theme
st.markdown("""
    <style>
    label , p{
        color: rgb(195 196 206);
        }
    .stApp {
        background-color: rgb(141 10 18);
        color:#fff;
    }
    .stButton>button {
        background-color: #0e0d0f;
        color: #fff;
    }
    .stAlert {
    background-color: lightgoldenrodyellow;
    color: #000;
    }
    </style>
""", unsafe_allow_html=True)
# Function to display peak ordering times
def show_peak_order_times():
    data = db.fetch_peak_order_times()
    peak_times = pd.DataFrame(data, columns=["Order Hour", "Order Count"])
    st.write("Peak Ordering Times (by hour)")
    st.bar_chart(peak_times.set_index("Order Hour"))

# Function to display top locations for orders
def show_top_locations_for_orders():
    data = db.fetch_top_locations_for_orders()
    locations = pd.DataFrame(data, columns=["Location", "Order Count"])
    st.write("Top Locations for Orders")
    st.bar_chart(locations.set_index("Location"))

# Function to display delayed deliveries
def show_delayed_deliveries():
    data = db.fetch_delayed_deliveries()
    deliveries = pd.DataFrame(data, columns=["Order ID", "Order Date", "Delivery Time", "Delay Duration (mins)"])
    st.write("Delayed Deliveries (over 30 minutes)")
    st.table(deliveries)

# Function to display top customers
def show_top_customers():
    data = db.fetch_top_customers()
    top_customers = pd.DataFrame(data, columns=["Customer ID", "Order Count"])
    st.write("Top Customers by Order Frequency")
    st.bar_chart(top_customers.set_index("Customer ID"))

# Function to display customer preferences (e.g., preferred cuisine)
def show_customer_preferences():
    data = db.fetch_customer_preferences()
    preferences = pd.DataFrame(data, columns=["Preferred Cuisine", "Order Count"])
    st.write("Customer Preferences (Cuisine Types)")
    st.bar_chart(preferences.set_index("Preferred Cuisine"))

# Function to show orders by location (map visualization)
def show_orders_by_location():
    data = db.fetch_orders_by_location()
    locations = pd.DataFrame(data, columns=["Location", "Order Count"])
    st.write("Orders by Location (Visualized on Map)")
    #st.map(locations)

# Function to show orders by value (top orders)
def show_orders_by_value():
    data = db.fetch_orders_by_value()
    orders_by_value = pd.DataFrame(data, columns=["Order ID", "Order Value"])
    st.write("Top Orders by Value")
    st.table(orders_by_value)
    
# Function to display customers
def show_customers():
    customers = db.fetch_customers()
    st.write("Customer Records")
    customer_df = pd.DataFrame(customers, columns=["Customer ID", "Name", "Email", "Phone", "Location", 
    "Signup Date", "Is Premium", "Preferred Cuisine", 
    "Total Orders", "Average Rating"])
    st.dataframe(customer_df.style.hide(axis="index"))

# Function to display orders
def show_orders():
    orders = db.fetch_orders()
    st.write("Order Records")
    order_df = pd.DataFrame(orders, columns=["Order ID", "Customer ID", "Restaurant ID", "Order Date",  "delivery_time", "status","Order Value","payment_mode", "discount_applied", "feedback_rating" ])
    st.dataframe(order_df.style.hide(axis="index"))

# Function to display restaurants
def show_restaurants():
    restaurants = db.fetch_restaurants()
    st.write("Restaurant Records")
    restaurant_df = pd.DataFrame(restaurants, columns=["Restaurant ID", "Name", "cuisine_type", "Location", "owner_name", "average_delivery_time", "contact_number", "rating", "total_orders", "is_active"])
    st.dataframe(restaurant_df.style.hide(axis="index"))

# Add Customer Form
def add_customer_form():
    st.header("Add New Customer")
    name = st.text_input("Customer Name")
    email  = st.text_input("Email")
    phone = st.text_input("Phone")
    location = st.text_input("Location")
    signup_date = st.text_input("Date")
    preferred_cuisine = st.text_input("preferred_cuisine")
    average_rating = st.text_input("Rating")

    if st.button("Add Customer"):
        if name and email and phone and location and signup_date:
            db.add_customer(name, email, phone, location, signup_date, preferred_cuisine, 0, average_rating)
            st.success("Customer added successfully!", icon="✔")
        else:
            st.error("Please fill all fields.", icon="⚠")

# Add Order Form
def add_order_form():
    st.header("Add New Order")
    customer_id = st.number_input("Customer ID", min_value=1)
    restaurant_id = st.number_input("Restaurant ID", min_value=1)
    order_date = st.date_input("Order Date", value=datetime.today())
    order_value = st.number_input("Order Value", min_value=0.0)
    if st.button("Add Order"):
        if customer_id and restaurant_id and order_value > 0:
            db.add_order(customer_id, restaurant_id, order_date, order_value)
            st.success("Order added successfully!")
        else:
            st.error("Please fill all fields.")

# Add Restaurant Form
def add_restaurant_form():
    st.header("Add New Restaurant")
    restaurant_name = st.text_input("Restaurant Name")
    location = st.text_input("Restaurant Location")
    if st.button("Add Restaurant"):
        if restaurant_name and location:
            db.add_restaurant(restaurant_name, location)
            st.success("Restaurant added successfully!")
        else:
            st.error("Please fill all fields.")

# Search Customers
def search_customers():
    st.header("Search Customers")
    search_term = st.text_input("Search by Name")
    if search_term:
        customers = db.search_customers(search_term)
        st.write("Search Results")
        customer_df = pd.DataFrame(customers, columns=["Customer ID", "Name", "Email", "Phone", "Location", 
    "Signup Date", "Is Premium", "Preferred Cuisine", 
    "Total Orders", "Average Rating"])
        st.dataframe(customer_df)
    else:
        st.write("Enter a search term.")

# Dynamic Table and Column Creation
def dynamic_table_creation():
    st.header("Create New Table or Add Column")
    action = st.selectbox("Choose an action", ["Create Table", "Add Column"])
    
    if action == "Create Table":
        table_name = st.text_input("Table Name")
        column_name = st.text_input("Column Name")
        column_type = st.selectbox("Column Type", ["VARCHAR(255)", "INT", "DATE", "FLOAT"])
        if st.button("Create Table"):
            if table_name and column_name:
                db.create_table(table_name, {column_name: column_type})
                st.success(f"Table {table_name} created successfully!")
            else:
                st.error("Please provide table name and column name.")
    
    elif action == "Add Column":
        table_name = st.text_input("Table Name")
        column_name = st.text_input("Column Name")
        column_type = st.selectbox("Column Type", ["VARCHAR(255)", "INT", "DATE", "FLOAT"])
        if st.button("Add Column"):
            if table_name and column_name:
                db.add_column(table_name, column_name, column_type)
                st.success(f"Column {column_name} added to {table_name} successfully!")
            else:
                st.error("Please provide table name and column name.")
                
            
# Function to delete a table
def delete_table():
    st.header("Delete Table")
    table_name = st.text_input("Table Name to Delete")
    if st.button("Delete Table"):
        if table_name:
            db.execute_query(f"DROP TABLE IF EXISTS {table_name}")
            st.success(f"Table {table_name} deleted successfully!", icon="✔")
        else:
            st.error("Please specify the table name.", icon="⚠")

# Function to delete a column
def delete_column():
    st.header("Delete Column from Table")
    table_name = st.text_input("Table Name")
    column_name = st.text_input("Column Name to Delete")
    if st.button("Delete Column"):
        if table_name and column_name:
            db.execute_query(f"ALTER TABLE {table_name} DROP COLUMN {column_name}")
            st.success(f"Column {column_name} deleted from {table_name} successfully!", icon="✔")
        else:
            st.error("Please provide both table and column names.", icon="⚠")
            
# Main function for the app layout
def main():
    st.title("Zomato - Food Delivery Data Insights")
    
    st.image("bg.webp")

    menu = ["Dashboard", "Add Customer", "Add Order", "Add Restaurant", "View Customers", "View Orders", "View Restaurants", "Create Table", "Add Column","Delete Table", "Delete Column", "Search Customers"]
    choice = st.sidebar.radio("Select Action", menu)

    if choice == "Dashboard":
        #st.header("Welcome to Zomato Data Insights Dashboard!")
        st.subheader("Manage your food delivery data seamlessly.")
        st.write("Use the sidebar to interact with the database.")
        #show_peak_order_times()
        #show_top_locations_for_orders()
        
        
    elif choice == "Add Customer":
        add_customer_form()

    elif choice == "Add Order":
        add_order_form()

    elif choice == "Add Restaurant":
        add_restaurant_form()

    elif choice == "View Customers":
        show_customers()

    elif choice == "View Orders":
        show_orders()

    elif choice == "View Restaurants":
        show_restaurants()

    elif choice == "Create Table" or choice == "Add Column":
        dynamic_table_creation()
        
    elif choice == "Delete Table":
        delete_table()

    elif choice == "Delete Column":
        delete_column()

    elif choice == "Search Customers":
        search_customers()

if __name__ == "__main__":
    main()
