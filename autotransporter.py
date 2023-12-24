import mysql.connector

# Database connection details
db_params = {
    "host": "localhost",
    "database": "gtfl",
    "user": "root",
    "password": "K1pd3K23",
}

# SQL query
query = """
    SELECT p.vehicle, p.route, p.date, p.fieldweight, p.factoryweight, pr.trans_pay 
    FROM pervehicle p
    LEFT JOIN prices pr ON p.route = pr.route
    WHERE p.date BETWEEN '2023-01-01' AND '2023-01-31';
"""

# Function to calculate the product and insert into the transporterpay table
def calculate_and_insert(cursor, result):
    for row in result:
        vehicle, route, date, fieldweight, factoryweight, trans_pay = row
        product = factoryweight * trans_pay

        # Insert into transporterpay table
        insert_query = """
            INSERT INTO transporterpay (vehicle, route, date, fieldweight, factoryweight, trans_pay, product)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (vehicle, route, date, fieldweight, factoryweight, trans_pay, product))

# Connect to the database
try:
    connection = mysql.connector.connect(**db_params)
    cursor = connection.cursor()

    # Execute the SELECT query
    cursor.execute(query)
    result = cursor.fetchall()

    # Create transporterpay table if not exists
    create_table_query = """
        CREATE TABLE IF NOT EXISTS transporterpay (
            vehicle VARCHAR(50),
            route VARCHAR(50),
            date DATE,
            fieldweight FLOAT,
            factoryweight FLOAT,
            trans_pay FLOAT,
            product FLOAT
        );
    """
    cursor.execute(create_table_query)

    # Calculate the product and insert into transporterpay table
    calculate_and_insert(cursor, result)

    # Commit the changes
    connection.commit()

    print("Query executed successfully and data inserted into transporterpay table.")

except (Exception, mysql.connector.Error) as error:
    print("Error:", error)

finally:
    # Close the database connection
    if connection:
        cursor.close()
        connection.close()
