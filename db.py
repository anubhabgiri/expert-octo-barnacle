import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv
load_dotenv()

# Database connection parameters
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

# Connect to the PostgreSQL database
def connect_db():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    return conn

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    create_table_query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS emails (
            id SERIAL PRIMARY KEY,
            email_id VARCHAR(255) NOT NULL,
            email_from VARCHAR(255) NOT NULL,
            subject VARCHAR(255) NOT NULL,
            received_date TIMESTAMP NOT NULL
        )
    """)
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()

# Create a new record
def create_record(email_from, subject, received_date):
    conn = connect_db()
    cursor = conn.cursor()
    insert_query = sql.SQL("INSERT INTO emails (email_from, subject, received_date) VALUES (%s, %s, %s)")
    cursor.execute(insert_query, (email_from, subject, received_date))
    conn.commit()
    cursor.close()
    conn.close()

def create_records(li):
    insert_query = sql.SQL("INSERT INTO emails (email_id, email_from, subject, received_date) VALUES (%s, %s, %s, %s)")
    conn = connect_db()
    cursor = conn.cursor()
    for i in li:
        cursor.execute(insert_query, i)
    conn.commit()
    cursor.close()
    conn.close()

# Read records
def fetch_all_records():
    conn = connect_db()
    cursor = conn.cursor()
    select_query = sql.SQL("SELECT email_id, email_from, subject, received_date FROM emails")
    cursor.execute(select_query)
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records
