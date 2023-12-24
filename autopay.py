import mysql.connector

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="K1pd3K23",
    database="gtfl"
)

# Create a cursor
cursor = connection.cursor()

# Fetch data from pervehicle table
cursor.execute("SELECT * FROM pervehicle")
pervehicle_data = cursor.fetchall()

# Loop through pervehicle data
for row in pervehicle_data:
    route = row['route']  # Assuming 'route' is the column name for routes in pervehicle table

    # Run VLOOKUP-like operation
    cursor.execute("SELECT trans_pay FROM prices WHERE route = %s", (route,))
    result = cursor.fetchone()

    if result:
        trans_pay = result['trans_pay']
        factoryweight = row['factoryweight']  # Assuming 'factoryweight' is the column name for factoryweight in pervehicle table

        # Calculate GrossPay
        gross_pay = factoryweight * trans_pay

        # Insert data into transporterpay1 table with the new GrossPay column
        cursor.execute("INSERT INTO transporterpay1 (route, factoryweight, trans_pay, rates, GrossPay) VALUES (%s, %s, %s, %s, %s)",
                       (route, factoryweight, trans_pay, row['rates'], gross_pay))

# Commit changes and close connections
connection.commit()
cursor.close()
connection.close()
