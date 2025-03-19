import mysql.connector

# Database Connection Function
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Change as per your MySQL user
            password="divya2005",  # Change as per your MySQL password
            database="billing_db"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

# Function to Create Tables
def create_tables():
    conn = connect_db()
    if conn is None:
        print("Failed to connect to the database.")
        return

    cursor = conn.cursor()

    # Create Customers Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
    """)

    # Create Bills Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            total_amount DECIMAL(10,2),
            FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
    print("Tables created successfully!")

# Run table creation if the script is executed
if __name__ == "__main__":
    create_tables()


