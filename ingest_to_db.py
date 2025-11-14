import sqlite3
import pandas as pd
import os

# Define paths
DB_PATH = os.path.join('db', 'ecommerce.db')
DATA_DIR = 'data'

def create_tables(conn):
    """Create database tables with foreign key constraints."""
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Drop tables if they exist to ensure a clean slate
    cursor.executescript("""
    DROP TABLE IF EXISTS reviews;
    DROP TABLE IF EXISTS order_items;
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS products;
    DROP TABLE IF EXISTS users;
    """)

    # Create tables with schemas
    cursor.executescript("""
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        join_date TEXT NOT NULL
    );

    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL
    );

    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        order_date TEXT NOT NULL,
        total_amount REAL NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );

    CREATE TABLE order_items (
        order_item_id INTEGER PRIMARY KEY,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );

    CREATE TABLE reviews (
        review_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        rating INTEGER NOT NULL,
        review_text TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
    """)
    print("Tables created successfully.")
    conn.commit()

def ingest_data(conn):
    """Ingest CSV data into the SQLite database."""
    # The order of ingestion matters due to foreign key constraints
    csv_files = ['users.csv', 'products.csv', 'orders.csv', 'order_items.csv', 'reviews.csv']
    
    for file_name in csv_files:
        try:
            table_name = os.path.splitext(file_name)[0]
            file_path = os.path.join(DATA_DIR, file_name)
            
            df = pd.read_csv(file_path)
            
            # Use pandas to_sql to insert data
            df.to_sql(table_name, conn, if_exists='append', index=False)
            
            print(f"Successfully ingested data from {file_name} into {table_name} table.")
        except Exception as e:
            print(f"Error ingesting {file_name}: {e}")

def verify_counts(conn):
    """Print the row counts for each table for verification."""
    cursor = conn.cursor()
    tables = ['users', 'products', 'orders', 'order_items', 'reviews']
    
    print("\n--- Table Row Counts ---")
    for table in tables:
        count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"- {table}: {count} rows")
    print("------------------------")

def main():
    # Ensure the db directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = None
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(DB_PATH)
        
        # 1. Create tables with proper schema and foreign keys
        create_tables(conn)
        
        # 2. Ingest data from CSV files
        ingest_data(conn)
        
        # 3. Verify the row counts
        verify_counts(conn)
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()
            print("\nDatabase connection closed.")

if __name__ == "__main__":
    main()
