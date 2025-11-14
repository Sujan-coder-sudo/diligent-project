# E-commerce Synthetic Data Project (SQLite | Python)

This project demonstrates a complete A-SDLC workflow by generating synthetic e-commerce data, ingesting it into a SQLite database, and running SQL joins across multiple tables.

## 📌 Features

- ✔ 5 synthetic e-commerce datasets
- ✔ Automated ingestion into SQLite
- ✔ Clean relational schema with foreign keys
- ✔ Complex SQL joins for reporting
- ✔ Fully reproducible workflow

## 📁 Project Structure

```
.
├── data/
│   ├── users.csv
│   ├── products.csv
│   ├── orders.csv
│   ├── order_items.csv
│   └── reviews.csv
├── db/
│   └── ecommerce.db
├── generate_data.py
├── ingest_to_db.py
├── query.sql
└── README.md
```

## 🧪 Step 1 — Generate Synthetic Data

Run the `generate_data.py` script to create 5 synthetic CSV files in the `/data/` directory.

```bash
python generate_data.py
```

This will generate:
- `users.csv`
- `products.csv`
- `orders.csv`
- `order_items.csv`
- `reviews.csv`

## 🗄 Step 2 — Ingest CSV Files Into SQLite

Run the `ingest_to_db.py` script to load the CSV data into a SQLite database.

```bash
python ingest_to_db.py
```

This script:
- Loads all CSVs using `pandas`.
- Creates SQLite tables with a proper schema.
- Enforces foreign key constraints.
- Inserts the data into the tables.
- Verifies the ingestion by printing row counts.

The final database is saved at `/db/ecommerce.db`.

## 🧩 Step 3 — Run SQL Queries

The `query.sql` file contains two queries for analysis:

1.  **Detailed Order Breakdown**: Joins across `users`, `orders`, `order_items`, and `products` to produce a detailed line-item view.
2.  **Total Spend Per User**: Aggregates all purchases to calculate the total spend for each user.

Run the queries using the `sqlite3` CLI:

```bash
sqlite3 db/ecommerce.db < query.sql
```

## 📦 Technologies Used

- Python 3
- Pandas
- SQLite3
- SQL

## 🚀 How It Works

1.  **Data Generation**: The `generate_data.py` script creates fake e-commerce data that looks real and maintains relational integrity, simulating a real business database.
2.  **Database Ingestion**: The `ingest_to_db.py` script acts as a data pipeline, moving data from CSV files into a structured SQLite database. It ensures data types are correct and foreign keys are enforced.
3.  **SQL Joins**: The `query.sql` file tests the database by running meaningful business queries, demonstrating an understanding of relational structure, SQL joins, and reporting logic.
4.  **Version Control**: The entire project, including data, scripts, and the database, is version-controlled with Git and available on GitHub.