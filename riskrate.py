import mysql.connector
from mysql.connector import errorcode
import pandas as pd
from datetime import datetime

# Replace these with your actual database connection details
db_params = {
    "host": "localhost",
    "database": "gtfl",
    "user": "root",
    "password": "K1pd3K23",
}

def fetch_and_calculate():
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(**db_params)
        cursor = connection.cursor()

        # Fetch data from collections and prices tables
        query = """
            SELECT c.farmerno,
                   MONTH(c.date) AS month,
                   SUM(p.field_pay * c.fieldweight) AS total_payment
            FROM collections c
            JOIN prices p ON c.route = p.route
            WHERE c.date BETWEEN '2023-01-01' AND '2023-01-31'
            GROUP BY c.farmerno, month
        """
        cursor.execute(query)
        results = cursor.fetchall()

        # Create a DataFrame from the results
        columns = ["farmerno", "month", "total_payment"]
        df = pd.DataFrame(results, columns=columns)

        # Display the result
        print("farmerno | month | total_payment")
        print("--------------------------------")
        for row in results:
            print(f"{row[0]} | {row[1]} | {row[2]:.2f}")

        # Save the DataFrame to an Excel file
        file_name = "result_january.xlsx"
        df.to_excel(file_name, index=False)
        print(f"\nExcel file '{file_name}' created successfully.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Access denied.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Database does not exist.")
        else:
            print(f"Error: {err}")

    finally:
        # Close the database connection
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    fetch_and_calculate()
