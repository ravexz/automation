import pandas as pd
import psycopg2

# Replace these with your actual database connection details
db_params = {
    'host': 'localhost',
    'database': 'risk',
    'user': 'postgres',
    'password': 'K1pd3K23',
}

# Connect to the PostgreSQL database
conn = psycopg2.connect(**db_params)

# Replace 'your_table_name' with the actual table name
table_name = 'collections'

# Query to get the data
query = f"SELECT growerno, route, date FROM {table_name}"

# Read data into a DataFrame
df = pd.read_sql_query(query, conn)

# Convert 'date' column to datetime type
df['date'] = pd.to_datetime(df['date'])

# Filter growers with collections from multiple routes
multiple_routes = df.groupby('growerno')['route'].nunique() > 2
result_df = df[df['growerno'].isin(multiple_routes[multiple_routes].index)]

# Save the result to an Excel file
result_df.to_excel('multiple_routes.xlsx', index=False)

# Close the database connection
conn.close()

print("Excel file 'grower_multiple_routes.xlsx' has been generated.")
