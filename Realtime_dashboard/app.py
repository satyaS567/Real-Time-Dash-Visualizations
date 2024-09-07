import datetime
import pandas as pd
from sqlalchemy import create_engine, text

# Setup SQLAlchemy engine
engine = create_engine('sqlite:///example.db')

# Create tables using SQLAlchemy if they don't exist
with engine.connect() as conn:
    conn.execute(text('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            join_date DATE
        )
    '''))

    conn.execute(text('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            amount REAL,
            transaction_date DATE
        )
    '''))

# Insert sample data into the users table
users = [
    (1, 'Ramesh', 'ramesh@example.com', datetime.date(2024, 1, 1)),
    (2, 'Mohit', 'panday@example.com', datetime.date(2024, 2, 3)),
    (3, 'Sumit', 'sumit@example.com', datetime.date(2024, 3, 1)),
    (4, 'Kumit', 'tiwari@example.com', datetime.date(2024, 4, 6)),
    (5, 'Sohan', 'yadav@example.com', datetime.date(2024, 5, 3))
]

# Insert sample data into the transactions table
transactions = [
    (1, 1, 300.00, datetime.date(2024, 1, 1)),
    (2, 1, 200.00, datetime.date(2024, 2, 3)),
    (3, 2, 650.00, datetime.date(2024, 3, 9)),
    (4, 3, 450.00, datetime.date(2024, 4, 6)),
    (5, 4, 350.00, datetime.date(2024, 5, 11)),
    (6, 5, 200.00, datetime.date(2024, 6, 20)),
    (7, 1, 400.00, datetime.date(2024, 7, 15)),
    (8, 2, 500.00, datetime.date(2024, 8, 12)),
    (9, 3, 600.00, datetime.date(2024, 9, 13)),
    (10, 4, 700.00, datetime.date(2024, 10, 30))
]

# Insert data using SQLAlchemy
with engine.connect() as conn:
    conn.execute(text('DELETE FROM users'))
    conn.execute(text('DELETE FROM transactions'))

    for user in users:
        conn.execute(text('INSERT INTO users VALUES (:user_id, :name, :email, :join_date)'),
                     {'user_id': user[0], 'name': user[1], 'email': user[2], 'join_date': user[3]})

    for transaction in transactions:
        conn.execute(text('INSERT INTO transactions VALUES (:transaction_id, :user_id, :amount, :transaction_date)'),
                     {'transaction_id': transaction[0], 'user_id': transaction[1], 'amount': transaction[2], 'transaction_date': transaction[3]})

# Query users who joined within a specific date range
def query_users_by_date(start_date, end_date):
    query = text('''
        SELECT * FROM users
        WHERE join_date BETWEEN :start_date AND :end_date
    ''')
    with engine.connect() as conn:
        result = conn.execute(query, {'start_date': start_date, 'end_date': end_date})
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df

# Query total amount spent by each user
def total_amount_spent():
    query = text('''
        SELECT u.user_id, u.name, SUM(t.amount) AS total_spent
        FROM users u
        JOIN transactions t ON u.user_id = t.user_id
        GROUP BY u.user_id
    ''')
    with engine.connect() as conn:
        result = conn.execute(query)
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df

# Join users and transactions to generate a report
def user_report():
    query = text('''
        SELECT u.name, u.email, COALESCE(SUM(t.amount), 0) AS total_spent
        FROM users u
        LEFT JOIN transactions t ON u.user_id = t.user_id
        GROUP BY u.user_id
    ''')
    with engine.connect() as conn:
        result = conn.execute(query)
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df

# Find top 3 users who spent the most
def top_3_users():
    df = total_amount_spent()
    return df.nlargest(3, 'total_spent')

# Calculate average transaction amount
def average_transaction_amount():
    query = text('''
        SELECT AVG(amount) AS average_amount
        FROM transactions
    ''')
    with engine.connect() as conn:
        result = conn.execute(query)
        average = result.scalar()
    return average

# Identify users with no transactions
def users_with_no_transactions():
    query = text('''
        SELECT u.user_id, u.name, u.email
        FROM users u
        LEFT JOIN transactions t ON u.user_id = t.user_id
        WHERE t.transaction_id IS NULL
    ''')
    with engine.connect() as conn:
        result = conn.execute(query)
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df

if __name__ == "__main__":
    print("Users who joined between 2022-01-01 and 2022-05-01:")
    print(query_users_by_date('2022-01-01', '2022-05-01'))

    print("\nTotal amount spent by each user:")
    print(total_amount_spent())

    print("\nUser report with total amount spent:")
    print(user_report())

    print("\nTop 3 users who spent the most:")
    print(top_3_users())

    print("\nAverage transaction amount:")
    print(average_transaction_amount())

    print("\nUsers with no transactions:")
    print(users_with_no_transactions())
