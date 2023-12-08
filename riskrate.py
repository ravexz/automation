import pandas as pd
import pymysql.cursors

# Replace these with your actual database connection details
db_params = {
    'host': 'localhost',
    'database': 'collections',
    'user': 'root',
    'password': 'K1pd3K23',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}

# Connect to the MySQL database
conn = pymysql.connect(**db_params)

# Replace 'your_table_name' with the actual table name
table_name = 'farmers'

# Query to get the data
query = f"SELECT FarmerNo, Route, Date FROM {table_name}"

# Read data into a DataFrame, skipping the first row (header)
df = pd.read_sql_query(query, conn, header=0, skiprows=1)

# Convert 'Date' column to datetime type
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

# Filter growers with collections from multiple routes
multiple_routes = df.groupby('FarmerNo')['Route'].nunique() > 2
result_df = df[df['FarmerNo'].isin(multiple_routes[multiple_routes].index)]

# Save the result to an Excel file
result_df.to_excel('multiple_routes.xlsx', index=False)

# Example: Update a column in the MySQL table (replace with your actual update logic)
update_query = f"UPDATE {table_name} SET some_column = 'some_value' WHERE FarmerNo IN ({', '.join(map(str, result_df['FarmerNo']))})"
with conn.cursor() as cursor:
    cursor.execute(update_query)
    conn.commit()

# Close the database connection
conn.close()

print("Excel file 'multiple_routes.xlsx' has been generated, and data in MySQL has been updated.")
