import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Database connection details
DATABASE_URI = 'mysql+pymysql://root:@localhost/zomato_insights'

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URI)

# Directory containing the CSV files
csv_directory = r'C:\st_project1\zomato_insights\data'

# Mapping of CSV filenames to database table names
table_mapping = {
    "customers.csv": "customers",
    "restaurants.csv": "restaurants",
    "orders.csv": "orders",
    "deliveries.csv": "deliveries",
    "deliveries.csv": "deliveries",
   
}

# Loop through the table mapping and process each file
for csv_file, table_name in table_mapping.items():
    csv_file_path = os.path.join(csv_directory, csv_file)
    if os.path.exists(csv_file_path):  # Check if the CSV file exists
        print(f"Processing file: {csv_file}")
        try:
            # Load CSV data into a DataFrame
            data = pd.read_csv(csv_file_path)
            
            # Insert data into the corresponding table
            data.to_sql(table_name, con=engine, if_exists='append', index=False)
            print(f"Data from {csv_file} inserted into '{table_name}' table successfully!")
        except SQLAlchemyError as e:
            print(f"Error inserting data from {csv_file} into '{table_name}' table: {e}")
    else:
        print(f"File {csv_file} not found. Skipping.")

print("All data processing completed!")
